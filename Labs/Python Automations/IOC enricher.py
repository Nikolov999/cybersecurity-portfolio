"""
IOC Enricher
- Input: CSV with column 'indicator' (IP, domain, or hash)
- Output: CSV with VT/AbuseIPDB reputation fields
Requirements: pip install requests pandas
Set your API keys below.
"""

import time, requests, pandas as pd

VIRUSTOTAL_KEY = "VT_API_KEY_HERE"         # https://www.virustotal.com/gui/my-apikey
ABUSEIPDB_KEY = "ABUSEIPDB_API_KEY_HERE"   # https://www.abuseipdb.com/account/api

def vt_lookup(ioc: str) -> dict:
    headers = {"x-apikey": VIRUSTOTAL_KEY}
    if "." in ioc and ioc.replace(".", "").isdigit():  # crude IP check
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
    elif "." in ioc and not ioc.endswith((".exe",".dll",".bin")):
        url = f"https://www.virustotal.com/api/v3/domains/{ioc}"
    else:
        url = f"https://www.virustotal.com/api/v3/files/{ioc}"
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code != 200: return {"vt_status": r.status_code}
    data = r.json().get("data", {}).get("attributes", {})
    stats = data.get("last_analysis_stats", {})
    return {
        "vt_harmless": stats.get("harmless"),
        "vt_malicious": stats.get("malicious"),
        "vt_suspicious": stats.get("suspicious"),
        "vt_undetected": stats.get("undetected"),
        "vt_reputation": data.get("reputation"),
    }

def abuseipdb_lookup(ip: str) -> dict:
    if not ip.replace(".", "").isdigit(): return {}
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    r = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=20)
    if r.status_code != 200: return {"abuse_status": r.status_code}
    data = r.json().get("data", {})
    return {
        "abuse_score": data.get("abuseConfidenceScore"),
        "abuse_total_reports": data.get("totalReports"),
        "abuse_last_reported": data.get("lastReportedAt"),
        "abuse_usage_type": data.get("usageType"),
    }

def enrich_file(in_csv: str, out_csv: str):
    df = pd.read_csv(in_csv)
    out_rows = []
    for i, row in df.iterrows():
        ioc = str(row["indicator"]).strip()
        vt = vt_lookup(ioc) if VIRUSTOTAL_KEY else {}
        ab = abuseipdb_lookup(ioc) if ABUSEIPDB_KEY else {}
        out = {"indicator": ioc, **vt, **ab}
        out_rows.append(out)
        time.sleep(15)  # respect public API rate limits
    pd.DataFrame(out_rows).to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Example: python ioc_enricher.py input.csv output.csv
    import sys
    enrich_file(sys.argv[1], sys.argv[2])

#How to run
cd Tools/Automation
pip install pandas requests
python ioc_enricher.py iocs.csv enriched.csv

