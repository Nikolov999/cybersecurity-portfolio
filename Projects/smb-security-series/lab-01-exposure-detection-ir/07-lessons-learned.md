# Lessons learned

## Prevention

* Remove plaintext secrets from shares
* Least privilege for Share + NTFS
* Access review for shared resources

## Detection (theoretical improvement, no tuning in Lab 01)

* Correlate: SMB access from unusual host → new network logon → remote service creation
