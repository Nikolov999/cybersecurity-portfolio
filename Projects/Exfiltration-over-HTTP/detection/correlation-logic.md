Correlation Logic:

1. Detect certutil execution
2. Validate outbound HTTP
3. Confirm file write location
4. Confirm privileged object access
5. Confirm logon context
6. Alert if chained within 2 minutes

Reason:
Single-event rules generate noise.
Chaining produces high-confidence detection.
