from __future__ import annotations

import json
import platform
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

def is_windows() -> bool:
    return platform.system().lower() == "windows"

def _run_powershell(cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
    p = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def _get_os() -> Optional[Dict[str, Any]]:
    name = "Windows"
    release = platform.release()
    build = platform.version()
    return {"name": name, "release": release, "build": build}

def _reboot_pending() -> bool:
    # Common registry indicators
    ps = r"""
$pending = $false
$keys = @(
 "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending",
 "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired",
 "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager"
)
foreach($k in $keys){
  if(Test-Path $k){
    if($k -like "*Session Manager*"){
      $v = (Get-ItemProperty $k -ErrorAction SilentlyContinue).PendingFileRenameOperations
      if($v){ $pending = $true }
    } else { $pending = $true }
  }
}
$pending | ConvertTo-Json
"""
    rc, out, _ = _run_powershell(ps, timeout=15)
    if rc == 0 and out:
        try:
            return bool(json.loads(out))
        except Exception:
            pass
    return False

def _hotfix_info() -> Optional[Dict[str, Any]]:
    ps = r"""
$h = Get-HotFix -ErrorAction SilentlyContinue
if(-not $h){ @{ installed_count = 0; last_installed_on = $null } | ConvertTo-Json; exit }
$last = $h | Sort-Object InstalledOn -Descending | Select-Object -First 1
@{
  installed_count = ($h | Measure-Object).Count
  last_installed_on = if($last.InstalledOn){ ($last.InstalledOn.ToString("yyyy-MM-dd")) } else { $null }
} | ConvertTo-Json
"""
    rc, out, _ = _run_powershell(ps, timeout=30)
    if rc == 0 and out:
        try:
            return json.loads(out)
        except Exception:
            return None
    return None

def _missing_updates_best_effort() -> List[Dict[str, Any]]:
    # Prefer PSWindowsUpdate if installed; otherwise return empty.
    ps = r"""
$missing = @()
if(Get-Module -ListAvailable -Name PSWindowsUpdate){
  Import-Module PSWindowsUpdate | Out-Null
  $u = Get-WindowsUpdate -MicrosoftUpdate -IgnoreReboot -AcceptAll -ErrorAction SilentlyContinue
  foreach($x in $u){
    $kb = $null
    if($x.KB){ $kb = ("KB" + ($x.KB -join ",")) }
    $missing += @{ kb = $kb; cve = $null }
  }
}
$missing | ConvertTo-Json
"""
    rc, out, _ = _run_powershell(ps, timeout=60)
    if rc == 0 and out:
        try:
            data = json.loads(out)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []

def _defender_status_best_effort() -> Dict[str, Any]:
    ps = r"""
$mp = Get-MpComputerStatus -ErrorAction SilentlyContinue
if(-not $mp){ @{} | ConvertTo-Json; exit }
@{
  av_enabled = $mp.AntivirusEnabled
  real_time_protection = $mp.RealTimeProtectionEnabled
  signatures_out_of_date = $mp.AntispywareSignatureOutOfDate -or $mp.AntivirusSignatureOutOfDate
  last_quick_scan = if($mp.QuickScanEndTime){ $mp.QuickScanEndTime.ToString("o") } else { $null }
} | ConvertTo-Json
"""
    rc, out, _ = _run_powershell(ps, timeout=20)
    if rc == 0 and out:
        try:
            return json.loads(out)
        except Exception:
            return {}
    return {}

def collect_windows_snapshot_parts() -> Tuple[Optional[Dict[str,Any]], bool, List[Dict[str,Any]], Optional[Dict[str,Any]], Dict[str,Any]]:
    os_part = _get_os()
    reboot_pending = _reboot_pending()
    missing_updates = _missing_updates_best_effort()
    hotfix = _hotfix_info()

    extras: Dict[str, Any] = {
        "defender_status_best_effort": _defender_status_best_effort(),
    }
    return os_part, reboot_pending, missing_updates, hotfix, extras
