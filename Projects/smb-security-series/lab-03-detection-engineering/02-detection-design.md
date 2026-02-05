# \## Detection Design

# 

# Detection is based on correlating three independent signals:

# 

# 1\. Network authentication (Event ID 4624, Logon Type 3)

# 2\. Privileged token assignment (Event ID 4672)

# 3\. Remote service creation (Event ID 4697 / 7045)

# 

# Rationale:

# Individually, these events are benign.

# Together, within a short timeframe, they indicate credential reuse and lateral movement.

# 

