"""
Zeek conn.log summarizer (TSV)
- Input: conn.log (space-delimited, with field names in a '#fields' line)
- Output: CSV with top talkers, services, failed conns
"""

import pandas as pd, re

def parse_zeek_conn(path: str) -> pd.DataFrame:
    rows, fields = [], []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split()[1:]
                continue
            if line.startswith("#") or not line.strip():
                continue
            parts = re.split(r"\\t|\\s{1,}", line.strip())
            if len(parts) == len(fields):
                rows.append(dict(zip(fields, parts)))
    df = pd.DataFrame(rows)
    return df

def summarize(path: str, out_prefix: str):
    df = parse_zeek_conn(path)
    # top external destinations
    top_dsts = df.groupby("id.resp_h").size().sort_values(ascending=False).head(20)
    top_svc = df.groupby("service").size().sort_values(ascending=False).head(20)
    fails = df[df.get("conn_state","").isin(["S0","REJ","RSTR"])].groupby("id.resp_h").size().sort_values(ascending=False).head(20)
    top_dsts.to_csv(out_prefix+"_top_dsts.csv")
    top_svc.to_csv(out_prefix+"_top_services.csv")
    fails.to_csv(out_prefix+"_failed_conns.csv")

if __name__ == "__main__":
    import sys
    summarize(sys.argv[1], sys.argv[2])

