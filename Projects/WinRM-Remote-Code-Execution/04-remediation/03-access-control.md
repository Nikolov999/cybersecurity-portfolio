\# Access Control (WinRM)



Goal: restrict who can remote into `192.168.1.32` and from where.



\## 1) Use a Dedicated Remote Management Account (Lab)

Create a standard user and grant remote management rights (not full admin unless needed):

```powershell

net user winrm\_operator "StrongPasswordHere!" /add

net localgroup "Remote Management Users" winrm\_operator /add

