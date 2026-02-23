# Detection Analysis

## Observed Pattern

Repeated DNS queries to echopentest.com
at consistent 510 second intervals.

## Indicators of Beaconing

- Stable periodic timing
- Same domain repeatedly queried
- Same host generating traffic
- Consistent resolver (8.8.8.8)
- Mixed success/failure events

## Why This Matters

Real malware frequently uses DNS
to maintain command-and-control channels
because DNS is rarely blocked.

Periodic repetition is a strong anomaly indicator.
