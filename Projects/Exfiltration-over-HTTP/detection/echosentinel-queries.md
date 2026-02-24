# Process Creation  certutil HTTP

index=windows EventCode=1 Image="*certutil.exe*" CommandLine="*http*"

# Security 4688  certutil

index=windows EventCode=4688 NewProcessName="*certutil.exe*"

# Privileged Object Access

index=windows EventCode=4673 OR EventCode=4674

# Correlated Burst (Process + Network)

(index=windows EventCode=1 Image="*certutil.exe*")
OR (index=windows EventCode=4688 NewProcessName="*certutil.exe*")
| transaction host maxspan=2m
