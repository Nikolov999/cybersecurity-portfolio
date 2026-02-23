# Lab Commands

## Configure DNS Server

Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 8.8.8.8

## Clear DNS Cache

Clear-DnsClientCache

## Simulate DNS Beacon

while ($true) {
    Resolve-DnsName -Name echopentest.com -Type A -DnsOnly -Server 8.8.8.8 | Out-Null
    Start-Sleep -Seconds 10
}

This loop generates periodic DNS queries to simulate C2 beaconing.
