# Telemetry Mapping

## Windows Event Source

Channel:
Microsoft-Windows-DNS-Client/Operational

## Event IDs Used

3006  DNS query issued  
3008  Successful resolution  
3010  Query failure  
3018  Timeout  

## C2 Simulation Characteristics

- Periodic repetition
- Domain frequency anomaly
- Reverse lookup noise (expected)
- CDN multi-IP resolution (normal behavior)

These logs provide sufficient data
to detect DNS-based C2 activity.
