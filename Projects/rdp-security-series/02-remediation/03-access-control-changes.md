\# RDP Security Series – 02 Remediation  

\## 03 – Access Control



\### Objective

Limit RDP access to authorized users and controlled network paths.



---



\## 1. Restrict RDP Group Membership



Review members:



```powershell

Get-LocalGroupMember -Group "Remote Desktop Users"



Remove unnecessary users:



```Powershell

Remove-LocalGroupMember `

-Group "Remote Desktop Users" `

-Member "username"



```



---



\## 2. Implement Least Privilege



* Do not grant Domain Admins direct RDP unless required



* Use dedicated jump-host accounts



* Separate admin and standard accounts



---



\## 3. IP-Based Access Control



Firewall rule restricted to management subnet:



```Powershell

New-NetFirewallRule `

-DisplayName "Restricted RDP" `

-Direction Inbound `

-Protocol TCP `

-LocalPort 3389 `

-RemoteAddress 10.10.10.0/24 `

-Action Allow



```



---



\## 4. Network Segmentation



Recommended architecture:



* Management VLAN



* Server VLAN



* Workstation VLAN



RDP only allowed from Management VLAN.



---



\## 5. Conditional Access (Enterprise Subnet)



If domain joined:



* Enforce MFA for RDP gateway



* Restrict login hours



* Monitor privileged sessions



---



\## Security Impact



* Reduced lateral movement paths



* Reduced credential exposure



* Enforced role-based access model



* Improved detection clarity for failed logon bursts
