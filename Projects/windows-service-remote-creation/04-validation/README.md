# 04  Validation

## Retest objectives
- Reproduce the chain and confirm EchoSentinel captures:
  - sc.exe create
  - registry ImagePath set
  - service install event
  - payload drop
  - service start
  - payload execution + child spawn

## Pass criteria
- Data quality: command lines, parent/child, file paths, registry target objects visible
- Alerts (if created): trigger on correlations, not single noisy events
