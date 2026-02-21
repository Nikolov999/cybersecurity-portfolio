# 01  Attack chain (Remote Service Creation)

## Goal
Create a Windows service remotely, point it to/associate it with a staged payload path, start it, and confirm execution.

## Expected evidence sequence
1. Successful logon (remote auth)
2. `sc.exe create ...`
3. Registry ImagePath/config change
4. Service installed event
5. Payload dropped to ProgramData
6. `sc.exe start ...`
7. Payload executed
8. Child process evidence / impact artifact created
