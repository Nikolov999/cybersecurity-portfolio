 # Process Chains (What to Expect)



 ## Canonical WinRM Execution Chain

One common pattern on the target:

 - `svchost.exe` (WinRM service host)

 - `wsmprovhost.exe` (WinRM provider host)

 - child process (depending on what you execute)

 - `powershell.exe`

 - `cmd.exe`

 - `conhost.exe` (console host)



 ## High-Signal Anchors

 - `wsmprovhost.exe` existence during attack window

 - Child process command line content (if collected)

 - Parent/child relationships:

  - Parent = `wsmprovhost.exe`

  - Child = `powershell.exe` / `cmd.exe`



 ## What to Capture as Evidence

 - Process creation event showing:

  - Image = `wsmprovhost.exe` and/or child image

  - ParentImage relationship

  - CommandLine fields



 ## Common Attack Commands (Script Block Evidence)

 - `Invoke-Command`

 - `Enter-PSSession`

 - `New-PSSession`

 - `Invoke-WebRequest`

 - `DownloadString`

 - `IEX`


