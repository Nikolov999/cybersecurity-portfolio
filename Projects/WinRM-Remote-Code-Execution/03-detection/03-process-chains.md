\# Process Chains (What to Expect)



\## Canonical WinRM Execution Chain

One common pattern on the target:

\- `svchost.exe` (WinRM service host)

&nbsp; → `wsmprovhost.exe` (WinRM provider host)

&nbsp;   → child process (depending on what you execute)

&nbsp;     - `powershell.exe`

&nbsp;     - `cmd.exe`

&nbsp;     - `conhost.exe` (console host)



\## High-Signal Anchors

\- `wsmprovhost.exe` existence during attack window

\- Child process command line content (if collected)

\- Parent/child relationships:

&nbsp; - Parent = `wsmprovhost.exe`

&nbsp; - Child = `powershell.exe` / `cmd.exe`



\## What to Capture as Evidence

\- Process creation event showing:

&nbsp; - Image = `wsmprovhost.exe` and/or child image

&nbsp; - ParentImage relationship

&nbsp; - CommandLine fields



\## Common Attack Commands (Script Block Evidence)

\- `Invoke-Command`

\- `Enter-PSSession`

\- `New-PSSession`

\- `Invoke-WebRequest`

\- `DownloadString`

\- `IEX`

