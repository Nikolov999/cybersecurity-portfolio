"""
Windows Failed-Login Triager
- Input: CSV of Windows Security Event 4625 exports with columns: TimeCreated, IpAddress, TargetUserName
- Output: Summary CSV of top offending IPs and accounts
Requirements: pip install pandas
Perfect for showing detecitons without Splunk
"""

import pandas as pd
from pathlib import Path

def summarize(in_csv: str, out_csv: str, window_minutes: int = 2, threshold: int = 5):
    df = pd.read_csv(in_csv, parse_dates=["TimeCreated"])
    df["window"] = (df["TimeCreated"].dt.floor(f"{window_minutes}T"))
    # count attempts by IP per window
    grouped = (df.groupby(["IpAddress", "window"])
                 .size()
                 .reset_index(name="failed_count"))
    suspects = grouped[grouped["failed_count"] >= threshold]
    # add top targeted users for each suspect IP
    top_users = (df[df["IpAddress"].isin(suspects["IpAddress"])]
                 .groupby(["IpAddress", "TargetUserName"])
                 .size().reset_index(name="count"))
    top_users = top_users.sort_values(["IpAddress","count"], ascending=[True,False]) \
                         .groupby("IpAddress").head(3)
    # save both
    suspects.to_csv(out_csv.replace(".csv","_suspects.csv"), index=False)
    top_users.to_csv(out_csv.replace(".csv","_top_users.csv"), index=False)

if __name__ == "__main__":
    import sys
    summarize(sys.argv[1], sys.argv[2])

