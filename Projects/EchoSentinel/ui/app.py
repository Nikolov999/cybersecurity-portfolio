import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from api import health, get_events, get_alerts
import streamlit.components.v1 as components
import html as _html
import json as _json
import base64 as _b64
import io as _io
import zipfile as _zipfile

st.set_page_config(page_title="EchoSentinel", layout="wide")


# -----------------------------
# Dark HTML tables (deterministic)
# -----------------------------
def dark_df(df: pd.DataFrame, height_px: int = 420):
    if df is None or df.empty:
        st.info("No data.")
        return
    safe = df.copy()
    html = safe.to_html(index=False, escape=True, classes="df-table")
    st.markdown(
        f"<div class='df-wrap' style='max-height:{int(height_px)}px'>{html}</div>",
        unsafe_allow_html=True,
    )


# -----------------------------
# Events table with client-side drawer (NO page reload, NO new tab)
# -----------------------------
def events_table_with_drawer_client(
    df_show: pd.DataFrame,
    df_full: pd.DataFrame,
    height_px: int = 720,
    key_col: str = "record_id",
):
    if df_show is None or df_show.empty:
        st.info("No data.")
        return

    cols = list(df_show.columns)

    head = "".join(f"<th>{_html.escape(str(c))}</th>" for c in cols)
    head += "<th style='text-align:right'>Open</th>"

    icon_svg = """
<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
     xmlns="http://www.w3.org/2000/svg" style="display:inline-block;vertical-align:middle">
  <path d="M10.5 18.5C14.6421 18.5 18 15.1421 18 11C18 6.85786 14.6421 3.5 10.5 3.5C6.35786 3.5 3 6.85786 3 11C3 15.1421 6.35786 18.5 10.5 18.5Z"
        stroke="rgba(255,255,255,1.0)" stroke-width="2"/>
  <path d="M20.5 20.5L16.9 16.9" stroke="rgba(255,255,255,1.0)" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

    body_rows = []
    for i in range(len(df_show)):
        row_show = df_show.iloc[i]

        # locate full row (raw + metadata)
        row_full = None
        key_val = str(i)
        if key_col in df_show.columns and key_col in df_full.columns:
            key_val = row_show.get(key_col, "")
            key_val = "" if pd.isna(key_val) else str(key_val)
            hit = df_full[df_full[key_col].astype(str) == str(key_val)]
            if not hit.empty:
                row_full = hit.iloc[0]
        if row_full is None and i < len(df_full):
            row_full = df_full.iloc[i]

        raw = ""
        if row_full is not None and "raw" in df_full.columns:
            raw = row_full.get("raw", "")
            raw = "" if pd.isna(raw) else str(raw)
        raw_b64 = _b64.b64encode(raw.encode("utf-8", errors="replace")).decode("ascii")

        ts = "" if row_full is None else row_full.get("timestamp", "")
        hn = "" if row_full is None else row_full.get("hostname", "")
        ts = "" if pd.isna(ts) else str(ts)
        hn = "" if pd.isna(hn) else str(hn)
        title = f"{ts} | {hn}".strip(" |") if (ts or hn) else "Event details"

        meta = {}
        if row_full is not None:
            for k in ["timestamp", "hostname", "event_id", "username", "source_ip", "channel", "record_id"]:
                if k in df_full.columns:
                    v = row_full.get(k, "")
                    meta[k] = "" if pd.isna(v) else str(v)

        meta_json = _json.dumps(meta, ensure_ascii=False)
        meta_json_esc = _html.escape(meta_json, quote=True)

        tds = []
        for c in cols:
            v = row_show.get(c, "")
            tds.append(f"<td>{_html.escape('' if pd.isna(v) else str(v))}</td>")

        open_cell = (
            "<td style=\"text-align:right; white-space:nowrap\">"
            f"<button class=\"open-ic eps-open\" type=\"button\" "
            f"data-title=\"{_html.escape(title, quote=True)}\" "
            f"data-meta=\"{meta_json_esc}\" "
            f"data-rawb64=\"{raw_b64}\" "
            f"aria-label=\"Open event\" "
            f"title=\"Open full message\">{icon_svg}</button>"
            "</td>"
        )

        body_rows.append("<tr>" + "".join(tds) + open_cell + "</tr>")

    table_html = f"""
<div class="df-wrap events-wrap" style="max-height:{int(height_px)}px">
  <table class="df-table">
    <thead><tr>{head}</tr></thead>
    <tbody>
      {''.join(body_rows)}
    </tbody>
  </table>
</div>

<div class="eps-overlay" id="eps-overlay" aria-hidden="true"></div>
<div class="eps-drawer" id="eps-drawer" role="dialog" aria-label="Event details" aria-hidden="true">
  <div class="eps-drawer-inner">
    <div class="eps-drawer-top">
      <div class="eps-drawer-title" id="eps-drawer-title">Event details</div>
      <button class="eps-drawer-close" id="eps-drawer-close" type="button" title="Close">Close</button>
    </div>
    <div class="eps-drawer-body">
      <div class="eps-kv" id="eps-kv"></div>
      <div class="eps-raw" id="eps-raw"></div>
    </div>
  </div>
</div>
"""
    st.markdown(table_html, unsafe_allow_html=True)

    components.html(
        """
<script>
(function(){
  const doc = (window.parent && window.parent.document) ? window.parent.document : document;

  if (doc.getElementById('eps-drawer-js-installed')) return;
  const mark = doc.createElement('div');
  mark.id = 'eps-drawer-js-installed';
  mark.style.display = 'none';
  doc.body.appendChild(mark);

  function qs(id){ return doc.getElementById(id); }

  function b64ToUtf8(b64){
    try{
      const bin = atob(b64 || '');
      const bytes = new Uint8Array(bin.length);
      for (let i=0;i<bin.length;i++) bytes[i] = bin.charCodeAt(i);
      return new TextDecoder('utf-8', { fatal:false }).decode(bytes);
    }catch(e){
      try{ return atob(b64 || ''); }catch(e2){ return ''; }
    }
  }

  function openDrawer(title, metaObj, rawText){
    const overlay = qs('eps-overlay');
    const drawer = qs('eps-drawer');
    const t = qs('eps-drawer-title');
    const kv = qs('eps-kv');
    const raw = qs('eps-raw');

    if (t) t.textContent = title || 'Event details';

    if (kv){
      kv.innerHTML = '';
      const keys = Object.keys(metaObj || {});
      for (let i=0;i<keys.length;i++){
        const k = keys[i];
        const kDiv = doc.createElement('div');
        kDiv.className = 'eps-k';
        kDiv.textContent = k;

        const vDiv = doc.createElement('div');
        vDiv.className = 'eps-v';
        vDiv.textContent = (metaObj[k] == null) ? '' : String(metaObj[k]);

        kv.appendChild(kDiv);
        kv.appendChild(vDiv);
      }
    }

    if (raw) raw.textContent = rawText || '';

    if (overlay) overlay.setAttribute('aria-hidden','false');
    if (drawer) drawer.setAttribute('aria-hidden','false');

    doc.body.classList.add('eps-drawer-on');
  }

  function closeDrawer(){
    const overlay = qs('eps-overlay');
    const drawer = qs('eps-drawer');
    if (overlay) overlay.setAttribute('aria-hidden','true');
    if (drawer) drawer.setAttribute('aria-hidden','true');
    doc.body.classList.remove('eps-drawer-on');
  }

  doc.addEventListener('click', function(e){
    const btn = e.target && e.target.closest ? e.target.closest('button.eps-open') : null;
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    const title = btn.getAttribute('data-title') || 'Event details';
    const metaRaw = btn.getAttribute('data-meta') || '{}';
    const rawB64 = btn.getAttribute('data-rawb64') || '';

    let metaObj = {};
    try{ metaObj = JSON.parse(metaRaw); }catch(err){ metaObj = {}; }

    const rawText = b64ToUtf8(rawB64);
    openDrawer(title, metaObj, rawText);
  }, true);

  const bindClose = function(){
    const closeBtn = qs('eps-drawer-close');
    const overlay = qs('eps-overlay');

    if (closeBtn && !closeBtn.dataset.bound){
      closeBtn.dataset.bound = '1';
      closeBtn.addEventListener('click', function(e){ e.preventDefault(); closeDrawer(); }, { passive:false });
    }
    if (overlay && !overlay.dataset.bound){
      overlay.dataset.bound = '1';
      overlay.addEventListener('click', function(e){ e.preventDefault(); closeDrawer(); }, { passive:false });
    }
  };

  bindClose();
  const obs = new MutationObserver(function(){ bindClose(); });
  obs.observe(doc.documentElement, { childList:true, subtree:true });

  doc.addEventListener('keydown', function(e){
    if (e.key === 'Escape') closeDrawer();
  });
})();
</script>
""",
        height=1,
    )


# -----------------------------
# Analyst additions (client-side, deterministic)
# -----------------------------
def derive_endpoints_from_events(events_df: pd.DataFrame, lookback_hours: int = 24) -> pd.DataFrame:
    if events_df is None or events_df.empty:
        return pd.DataFrame(columns=["hostname", "last_seen", "channels_seen", "sysmon_present", "event_rate"])

    df = events_df.copy()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    else:
        df["timestamp"] = pd.NaT

    if "hostname" not in df.columns:
        df["hostname"] = ""

    if "channel" not in df.columns:
        df["channel"] = ""

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=int(max(1, min(lookback_hours, 720))))

    df_recent = df[df["timestamp"] >= cutoff].copy()

    last_seen = (
        df.groupby("hostname", dropna=False)["timestamp"]
        .max()
        .reset_index()
        .rename(columns={"timestamp": "last_seen"})
    )

    chan = (
        df.groupby("hostname", dropna=False)["channel"]
        .apply(lambda s: sorted({str(x) for x in s.dropna().tolist() if str(x).strip()}))
        .reset_index()
        .rename(columns={"channel": "channels_seen"})
    )

    sysmon = (
        df.groupby("hostname", dropna=False)["channel"]
        .apply(lambda s: any("sysmon" in str(x).lower() for x in s.dropna().tolist()))
        .reset_index()
        .rename(columns={"channel": "sysmon_present"})
    )

    counts = (
        df_recent.groupby("hostname", dropna=False)
        .size()
        .reset_index(name="events_in_window")
    )
    hours = float(max(1, min(lookback_hours, 720)))
    counts["event_rate"] = counts["events_in_window"].astype(float) / hours
    counts = counts.drop(columns=["events_in_window"])

    out = last_seen.merge(chan, on="hostname", how="left").merge(sysmon, on="hostname", how="left").merge(counts, on="hostname", how="left")
    out["channels_seen"] = out["channels_seen"].apply(lambda v: v if isinstance(v, list) else [])
    out["sysmon_present"] = out["sysmon_present"].fillna(False).astype(bool)
    out["event_rate"] = out["event_rate"].fillna(0.0).astype(float)

    def _status(ts):
        if pd.isna(ts):
            return "unknown"
        age = now - ts.to_pydatetime()
        if age <= timedelta(minutes=30):
            return "online"
        if age <= timedelta(hours=24):
            return "stale"
        return "dead"

    out["status"] = out["last_seen"].apply(_status)
    out = out.sort_values("last_seen", ascending=False)
    return out[["hostname", "status", "last_seen", "sysmon_present", "event_rate", "channels_seen"]]


def dedup_alerts(alerts_df: pd.DataFrame) -> pd.DataFrame:
    if alerts_df is None or alerts_df.empty:
        return pd.DataFrame(
            columns=["severity", "rule_name", "hostname", "username", "source_ip", "details", "first_seen", "last_seen", "occurrences"]
        )

    df = alerts_df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    for c in ["severity", "rule_name", "hostname", "username", "source_ip", "details"]:
        if c not in df.columns:
            df[c] = ""

    for c in ["hostname", "username", "source_ip", "details", "rule_name", "severity"]:
        df[c] = df[c].astype(str).fillna("")

    gcols = ["severity", "rule_name", "hostname", "username", "source_ip", "details"]
    agg = (
        df.groupby(gcols, dropna=False)
        .agg(
            occurrences=("timestamp", "count"),
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
        )
        .reset_index()
        .sort_values(["last_seen", "occurrences"], ascending=[False, False])
    )
    return agg


def build_evidence_zip_bytes(alert_row: dict, related_events_df: pd.DataFrame) -> bytes:
    ts = alert_row.get("timestamp", "")
    hn = alert_row.get("hostname", "")
    rid = alert_row.get("rule_name", "")
    sev = alert_row.get("severity", "")
    details = alert_row.get("details", "")

    readme = (
        "EchoSentinel Evidence Bundle\n\n"
        f"Rule: {rid}\n"
        f"Severity: {sev}\n"
        f"Host: {hn}\n"
        f"Time: {ts}\n\n"
        "Why it fired:\n"
        f"- {details}\n\n"
        "Included artifacts:\n"
        "- alert.json: the selected alert row\n"
        "- events.jsonl: related raw events (±5 minutes, same host)\n"
        "- README.txt: this explanation\n"
    )

    mem = _io.BytesIO()
    with _zipfile.ZipFile(mem, "w", compression=_zipfile.ZIP_DEFLATED) as z:
        z.writestr("alert.json", _json.dumps(alert_row, indent=2, ensure_ascii=False, default=str))
        z.writestr("README.txt", readme)

        if related_events_df is None or related_events_df.empty:
            z.writestr("events.jsonl", "")
        else:
            cols_pref = ["timestamp", "hostname", "event_id", "username", "source_ip", "channel", "record_id", "raw"]
            cols = [c for c in cols_pref if c in related_events_df.columns] + [c for c in related_events_df.columns if c not in cols_pref]
            tmp = related_events_df[cols].copy()
            lines = []
            for _, r in tmp.iterrows():
                lines.append(_json.dumps({k: ("" if pd.isna(v) else v) for k, v in r.to_dict().items()}, ensure_ascii=False, default=str))
            z.writestr("events.jsonl", "\n".join(lines))

    mem.seek(0)
    return mem.getvalue()


# -----------------------------
# Global styles (force ALL text white + dropdown black + purple gradients incl. download button)
# -----------------------------
st.markdown(
    """
<style>
:root{
  --bg0:#0b0816;
  --bg1:#120c24;
  --text:#ffffff;
  --border: rgba(255,255,255,0.14);
  --radius: 16px;

  --purple1:#6d28d9;
  --purple2:#a855f7;
  --purple3:#c084fc;
  --cyan1:#22d3ee;
}

/* nuclear: everything defaults to white */
html, body, [class*="st-"], [data-testid], p, span, div, label, small, li, a, code, pre, h1, h2, h3, h4, h5, h6{
  color: #ffffff !important;
}

/* keep backgrounds */
div[data-testid="stDecoration"]{ background:#000 !important; }
header, [data-testid="stHeader"]{ background:#000 !important; }
[data-testid="stToolbar"]{ background:transparent !important; }

.stApp{
  background:
    radial-gradient(1200px 800px at 12% 8%, rgba(168,85,247,0.24) 0%, rgba(168,85,247,0.0) 58%),
    radial-gradient(1000px 700px at 88% 12%, rgba(34,211,238,0.18) 0%, rgba(34,211,238,0.0) 58%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg0) 78%, #070514 100%);
}

.block-container{
  padding-top: 2.1rem !important;
  padding-bottom: 2.0rem;
  max-width: 1280px;
}

/* Inputs */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div{
  background: rgba(0,0,0,0.80) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-baseweb="input"] input,
[data-baseweb="select"] input{
  color: #ffffff !important;
}
[data-baseweb="select"] span{ color: #ffffff !important; }
[data-baseweb="select"] svg{ fill: #ffffff !important; opacity: 0.92; }

/* Dropdown menu (black background + white text) */
div[data-baseweb="popover"]{
  color: #ffffff !important;
}
div[data-baseweb="popover"] div[role="listbox"],
ul[data-testid="stSelectboxVirtualDropdown"]{
  background: rgba(0,0,0,0.94) !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
}
div[data-baseweb="popover"] li[role="option"]{
  color: #ffffff !important;
  background: transparent !important;
}
div[data-baseweb="popover"] li[role="option"]:hover{
  background: rgba(168,85,247,0.22) !important;
}
div[data-baseweb="popover"] li[aria-selected="true"]{
  background: rgba(109,40,217,0.40) !important;
}

/* Buttons (ALL buttons including download button) */
.stButton > button,
div[data-testid="stDownloadButton"] button,
div[data-testid="stDownloadButton"] a{
  border-radius: 12px !important;
  border: 1px solid rgba(168,85,247,0.34) !important;
  background: linear-gradient(135deg, rgba(109,40,217,0.82) 0%, rgba(168,85,247,0.50) 55%, rgba(192,132,252,0.28) 100%) !important;
  color: #ffffff !important;
  font-weight: 900 !important;
  box-shadow: 0 14px 34px rgba(0,0,0,0.45);
}
.stButton > button:hover,
div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stDownloadButton"] a:hover{
  border-color: rgba(34,211,238,0.30) !important;
  background: linear-gradient(135deg, rgba(109,40,217,0.92) 0%, rgba(168,85,247,0.58) 55%, rgba(34,211,238,0.18) 100%) !important;
}

/* Header */
.eps-header{
  border: 1px solid rgba(255,255,255,0.12);
  background:
    linear-gradient(180deg, rgba(16,12,30,0.90) 0%, rgba(10,8,22,0.80) 100%),
    radial-gradient(900px 260px at 18% 40%, rgba(109,40,217,0.40) 0%, rgba(109,40,217,0.0) 60%),
    radial-gradient(900px 260px at 82% 40%, rgba(34,211,238,0.24) 0%, rgba(34,211,238,0.0) 60%);
  border-radius: 16px;
  padding: 28px 26px 22px 26px;
  box-shadow: 0 14px 46px rgba(0,0,0,0.55);
  margin: 18px 0 16px 0;
}
.eps-title{
  font-size: 34px;
  font-weight: 900;
  letter-spacing: 0.2px;
  margin: 0;
  line-height: 1.1;
}
.eps-sub{
  margin: 10px 0 0 0;
  font-size: 13px;
  opacity: 0.90;
}
.eps-pillrow{
  display:flex;
  gap:10px;
  margin-top: 16px;
  flex-wrap: wrap;
}
.eps-pill{
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(0,0,0,0.30);
  border-radius: 999px;
  padding: 7px 11px;
  font-size: 12px;
}
.eps-dot{
  display:inline-block;
  width:8px;
  height:8px;
  border-radius: 99px;
  margin-right: 8px;
  vertical-align: middle;
  background: rgba(255,255,255,0.35);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  gap: 8px;
  padding: 7px 7px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(0,0,0,0.50);
}
.stTabs [data-baseweb="tab"]{
  border-radius: 12px;
  padding: 10px 14px;
  color: #ffffff !important;
}
.stTabs [aria-selected="true"]{
  background: linear-gradient(135deg, rgba(109,40,217,0.52) 0%, rgba(168,85,247,0.26) 60%, rgba(34,211,238,0.12) 100%) !important;
  border: 1px solid rgba(34,211,238,0.22) !important;
}

/* Alerts container */
.stAlert{
  border-radius: 16px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(0,0,0,0.50) !important;
}

/* DARK HTML TABLES */
.df-wrap{
  background: rgba(12, 10, 26, 0.90);
  border: 1px solid rgba(170,120,255,0.22);
  border-radius: 14px;
  overflow: auto;
  max-width: 100%;
  box-shadow: 0 18px 55px rgba(0,0,0,0.35);
}
.df-table{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  color: #ffffff;
}
.df-table thead th{
  position: sticky;
  top: 0;
  z-index: 2;
  text-align: left;
  background: rgba(120, 60, 220, 0.34);
  color: #ffffff;
  font-weight: 900;
  padding: 10px 12px;
  border-bottom: 1px solid rgba(170,120,255,0.35);
  white-space: nowrap;
}
.df-table tbody td{
  padding: 10px 12px;
  border-bottom: 1px solid rgba(170,120,255,0.10);
  color: #ffffff;
  vertical-align: top;
  word-break: break-word;
}
.df-table tbody tr{ background: rgba(18, 14, 34, 0.78); }
.df-table tbody tr:nth-child(even){ background: rgba(22, 18, 40, 0.78); }
.df-table tbody tr:hover{ background: rgba(160, 90, 255, 0.18); }

.df-wrap::-webkit-scrollbar{ height: 10px; width: 10px; }
.df-wrap::-webkit-scrollbar-thumb{
  background: rgba(170,120,255,0.28);
  border-radius: 999px;
}
.df-wrap::-webkit-scrollbar-track{
  background: rgba(12, 10, 26, 0.55);
}

/* Open icon button */
.open-ic{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width: 34px;
  height: 28px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.14);
  background: linear-gradient(135deg, rgba(109,40,217,0.30) 0%, rgba(168,85,247,0.14) 60%, rgba(34,211,238,0.10) 100%);
  box-shadow: 0 10px 20px rgba(0,0,0,0.35);
  cursor:pointer;
  padding:0;
}
.open-ic:hover{
  border-color: rgba(34,211,238,0.30);
  background: linear-gradient(135deg, rgba(109,40,217,0.42) 0%, rgba(168,85,247,0.18) 60%, rgba(34,211,238,0.12) 100%);
}

/* RIGHT DRAWER */
.eps-overlay{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(6px);
  z-index: 9998;
  opacity: 0;
  pointer-events: none;
  transition: opacity 180ms ease;
}
.eps-drawer{
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: min(920px, 94vw);
  z-index: 9999;

  transform: translateX(103%);
  transition: transform 220ms ease;

  border-left: 1px solid rgba(255,255,255,0.14);
  background:
    linear-gradient(180deg, rgba(10,8,22,0.92) 0%, rgba(8,6,18,0.86) 100%),
    radial-gradient(1200px 520px at 12% 18%, rgba(109,40,217,0.52) 0%, rgba(109,40,217,0.0) 55%),
    radial-gradient(1200px 520px at 88% 18%, rgba(34,211,238,0.30) 0%, rgba(34,211,238,0.0) 55%);
}
.eps-drawer-inner{ height: 100%; display:flex; flex-direction:column; }
.eps-drawer-top{
  padding: 18px 18px 12px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap: 12px;
}
.eps-drawer-title{
  font-weight: 900;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.eps-drawer-close{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  height: 34px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.35);
  font-weight: 900;
}
.eps-drawer-close:hover{
  border-color: rgba(34,211,238,0.28);
  background: rgba(0,0,0,0.45);
}
.eps-drawer-body{ padding: 14px 18px 18px 18px; overflow:auto; flex:1; }
.eps-kv{ display:grid; grid-template-columns: 140px 1fr; gap: 8px 12px; margin-bottom: 14px; }
.eps-k{ font-size: 12px; opacity: 0.92; }
.eps-v{ font-size: 12px; word-break: break-word; }
.eps-raw{
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 14px;
  background: rgba(0,0,0,0.40);
  padding: 12px;
  font-size: 12px;
  line-height: 1.45;
  white-space: pre-wrap;
  word-break: break-word;
}

body.eps-drawer-on .eps-overlay{ opacity: 1; pointer-events:auto; }
body.eps-drawer-on .eps-drawer{ transform: translateX(0%); }
</style>
""",
    unsafe_allow_html=True,
)

components.html("<script>/* mounted */</script>", height=1)

st.markdown(
    """
<div class="eps-header">
  <div class="eps-title">EchoSentinel</div>
  <div class="eps-sub">Mini SIEM — collect → store → parse → detect → display</div>
  <div class="eps-pillrow">
    <div class="eps-pill"><span class="eps-dot" id="dot-backend"></span>Backend</div>
    <div class="eps-pill"><span class="eps-dot"></span>Window</div>
    <div class="eps-pill">SQLite</div>
    <div class="eps-pill">Auth + Persistence + Sysmon</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([2, 2, 6])

with col1:
    st.subheader("Backend")
    try:
        h = health()
        st.success(h.get("status", "ok"))
        st.markdown("<style>#dot-backend{background: rgba(34,197,94,0.88) !important;}</style>", unsafe_allow_html=True)
    except Exception:
        st.error("offline")
        st.markdown("<style>#dot-backend{background: rgba(239,68,68,0.88) !important;}</style>", unsafe_allow_html=True)

with col2:
    st.subheader("Window")
    now = datetime.now(timezone.utc)
    st.write(f"UTC: {now.strftime('%Y-%m-%d %H:%M:%S')}")


# -----------------------------
# Rule catalog (UI-only)
# -----------------------------
RULES_CATALOG = [
    {"pack": "Auth", "rule": "ES-AUTH-001", "severity": "medium", "signals": "4625", "default": "≥5 failures / 2 min per (source_ip, username)"},
    {"pack": "Auth", "rule": "ES-AUTH-002", "severity": "high", "signals": "4625", "default": "≥15 failures / 5 min per source_ip AND ≥6 usernames"},
    {"pack": "Auth", "rule": "ES-AUTH-003", "severity": "high", "signals": "4625(LogonType=10)", "default": "≥3 failures / 1 min per (source_ip, username)"},
    {"pack": "Auth", "rule": "ES-AUTH-004", "severity": "high/medium", "signals": "4624", "default": "same username, different source_ip within 10 min"},
    {"pack": "Auth", "rule": "ES-AUTH-005", "severity": "medium", "signals": "4624(LogonType 10/3)", "default": "privileged user logon type focus"},
    {"pack": "Auth", "rule": "ES-AUTH-006", "severity": "medium/low", "signals": "4624", "default": "first-seen (username, source_ip)"},
    {"pack": "Auth", "rule": "ES-AUTH-007", "severity": "high", "signals": "4648", "default": "explicit credentials used"},
    {"pack": "Auth", "rule": "ES-AUTH-008", "severity": "medium", "signals": "4672", "default": "special privileges at logon (not allowlisted)"},
    {"pack": "Persistence", "rule": "ES-PERS-001", "severity": "medium", "signals": "4697", "default": "new service installed"},
    {"pack": "Persistence", "rule": "ES-PERS-002", "severity": "high", "signals": "4697 + (7045/7036)", "default": "service installed then started within 2 min"},
    {"pack": "Persistence", "rule": "ES-PERS-003", "severity": "medium/high", "signals": "4698", "default": "scheduled task created; high if suspicious path"},
    {"pack": "Persistence", "rule": "ES-PERS-004", "severity": "high", "signals": "4732/4733", "default": "account added/removed from Administrators"},
    {"pack": "Persistence", "rule": "ES-PERS-005", "severity": "high", "signals": "4720", "default": "new user created"},
    {"pack": "Persistence", "rule": "ES-PERS-006", "severity": "high", "signals": "4722", "default": "user enabled"},
    {"pack": "Lateral", "rule": "ES-LAT-001", "severity": "medium", "signals": "4624", "default": "first-seen admin workstation→server pair"},
    {"pack": "Sysmon", "rule": "ES-SYS-001", "severity": "high", "signals": "Sysmon 1", "default": "winword.exe → powershell/wscript/cscript/mshta/rundll32/regsvr32"},
    {"pack": "Sysmon", "rule": "ES-SYS-002", "severity": "high", "signals": "Sysmon 1", "default": "LOLBins with network indicators (enc/urlcache/http)"},
    {"pack": "Sysmon", "rule": "ES-SYS-003", "severity": "medium/high", "signals": "Sysmon 11", "default": "file create in persistence paths"},
    {"pack": "Sysmon", "rule": "ES-SYS-004", "severity": "medium", "signals": "Sysmon 7", "default": "unsigned DLL load by sensitive process"},
]


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Events", "Alerts", "Endpoints", "Rules"])


@st.cache_data(ttl=5)
def load_data():
    ev = get_events(limit=1000)
    al = get_alerts(limit=1000)

    ev_df = pd.DataFrame(ev)
    al_df = pd.DataFrame(al)

    if not ev_df.empty:
        if "event_id" in ev_df.columns:
            ev_df["event_id"] = ev_df["event_id"].astype(str).str.replace(",", "", regex=False)
            ev_df["event_id"] = pd.to_numeric(ev_df["event_id"], errors="coerce")
        if "record_id" in ev_df.columns:
            ev_df["record_id"] = ev_df["record_id"].astype(str).str.replace(",", "", regex=False)
            ev_df["record_id"] = pd.to_numeric(ev_df["record_id"], errors="coerce")

    if not al_df.empty and "event_id" in al_df.columns:
        al_df["event_id"] = al_df["event_id"].astype(str).str.replace(",", "", regex=False)
        al_df["event_id"] = pd.to_numeric(al_df["event_id"], errors="coerce")

    if not ev_df.empty and "timestamp" in ev_df.columns:
        ev_df["timestamp"] = pd.to_datetime(ev_df["timestamp"], utc=True, errors="coerce")
    if not al_df.empty and "timestamp" in al_df.columns:
        al_df["timestamp"] = pd.to_datetime(al_df["timestamp"], utc=True, errors="coerce")

    return ev_df, al_df


ev_df, al_df = load_data()

with tab1:
    left, right = st.columns([3, 2])

    with left:
        st.subheader("Event counts (last 24h)")
        if ev_df.empty:
            st.info("No events yet.")
        else:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
            recent = ev_df[ev_df["timestamp"] >= cutoff]
            by_id = recent.groupby("event_id").size().reset_index(name="count").sort_values("count", ascending=False)
            dark_df(by_id, height_px=260)

    with right:
        st.subheader("Alerts (last 24h)")
        if al_df.empty:
            st.info("No alerts yet.")
        else:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
            recent = al_df[al_df["timestamp"] >= cutoff]
            by_sev = recent.groupby("severity").size().reset_index(name="count")
            dark_df(by_sev, height_px=260)

    st.subheader("Latest alerts")
    if al_df.empty:
        st.info("No alerts yet.")
    else:
        latest = al_df.sort_values("timestamp", ascending=False).head(20)
        cols = ["timestamp", "severity", "rule_name", "hostname", "username", "source_ip", "details"]
        cols = [c for c in cols if c in latest.columns]
        dark_df(latest[cols], height_px=420)

with tab2:
    st.subheader("Events")
    f1, f2, f3, f4 = st.columns([2, 2, 2, 4])
    with f1:
        host_filter = st.text_input("Hostname filter", value="")
    with f2:
        event_filter = st.text_input("Event ID filter", value="")
    with f3:
        user_filter = st.text_input("Username filter", value="")
    with f4:
        refresh = st.button("Refresh")

    if refresh:
        st.cache_data.clear()
        ev_df, al_df = load_data()

    df = ev_df.copy()
    if host_filter:
        df = df[df["hostname"].astype(str).str.contains(host_filter, case=False, na=False)]
    if event_filter.strip().isdigit():
        df = df[df["event_id"] == int(event_filter.strip())]
    if user_filter:
        df = df[df["username"].astype(str).str.contains(user_filter, case=False, na=False)]

    if df.empty:
        st.info("No matching events.")
    else:
        df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

        raw_series = df["raw"].astype(str).fillna("") if "raw" in df.columns else pd.Series([""] * len(df))
        msg = raw_series.str.replace("\r", " ", regex=False).str.replace("\n", " ", regex=False).str.strip()
        df["message"] = msg.apply(lambda s: (s[:180] + "…") if len(s) > 180 else s)

        show_cols = ["timestamp", "hostname", "event_id", "username", "source_ip", "channel", "record_id", "message"]
        show_cols = [c for c in show_cols if c in df.columns]
        view = df[show_cols].copy()

        events_table_with_drawer_client(view, df, height_px=720, key_col="record_id")

with tab3:
    st.subheader("Alerts")

    a1, a2, a3, a4 = st.columns([2, 2, 3, 3])
    with a1:
        host_a = st.text_input("Hostname", value="", key="host_a")
    with a2:
        sev = st.selectbox("Severity", ["", "low", "medium", "high"], index=0)
    with a3:
        pack = st.selectbox("Pack", ["", "Auth", "Persistence", "Lateral", "Sysmon"], index=0)
    with a4:
        refresh_a = st.button("Refresh Alerts")

    if refresh_a:
        st.cache_data.clear()
        ev_df, al_df = load_data()

    df = al_df.copy()
    if host_a:
        df = df[df["hostname"].astype(str).str.contains(host_a, case=False, na=False)]
    if sev:
        df = df[df["severity"] == sev]

    if pack:
        p = pack.strip().lower()
        prefix = {
            "auth": "ES-AUTH-",
            "persistence": "ES-PERS-",
            "lateral": "ES-LAT-",
            "sysmon": "ES-SYS-",
        }.get(p, "")
        if prefix and "rule_name" in df.columns:
            df = df[df["rule_name"].astype(str).str.contains(prefix, case=False, na=False)]

    if df.empty:
        st.info("No matching alerts.")
    else:
        st.caption("Deduplicated view (identical alerts collapsed into one row with an occurrences counter).")

        dedup = dedup_alerts(df)
        show_cols = ["last_seen", "severity", "rule_name", "hostname", "username", "source_ip", "occurrences", "first_seen", "details"]
        show_cols = [c for c in show_cols if c in dedup.columns]
        dark_df(dedup[show_cols], height_px=520)

        st.subheader("Evidence bundle export")
        st.caption("Exports: alert JSON, related raw events (±5 minutes, same host), and a README explaining the trigger.")

        raw_sorted = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

        if "id" in raw_sorted.columns:
            raw_sorted["__label"] = raw_sorted.apply(
                lambda r: f'{int(r.get("id"))} | {str(r.get("timestamp",""))} | {str(r.get("severity",""))} | {str(r.get("rule_name",""))} | {str(r.get("hostname",""))}',
                axis=1,
            )
            sel = st.selectbox("Select alert instance", raw_sorted["__label"].tolist(), index=0)
            sel_id = int(sel.split("|", 1)[0].strip())
            picked = raw_sorted[raw_sorted["id"] == sel_id].iloc[0].to_dict()
        else:
            raw_sorted["__label"] = raw_sorted.apply(
                lambda r: f'{str(r.get("timestamp",""))} | {str(r.get("severity",""))} | {str(r.get("rule_name",""))} | {str(r.get("hostname",""))}',
                axis=1,
            )
            sel = st.selectbox("Select alert instance", raw_sorted["__label"].tolist(), index=0)
            picked = raw_sorted[raw_sorted["__label"] == sel].iloc[0].to_dict()
            sel_id = 0

        ev_rel = ev_df.copy()
        if not ev_rel.empty and "timestamp" in ev_rel.columns:
            ev_rel["timestamp"] = pd.to_datetime(ev_rel["timestamp"], utc=True, errors="coerce")

        hn = str(picked.get("hostname", "") or "")
        ts = picked.get("timestamp", None)
        try:
            ts = pd.to_datetime(ts, utc=True, errors="coerce")
        except Exception:
            ts = pd.NaT

        if hn and ev_rel is not None and not ev_rel.empty and not pd.isna(ts):
            t0 = ts - timedelta(minutes=5)
            t1 = ts + timedelta(minutes=5)
            rel = ev_rel[(ev_rel["hostname"].astype(str) == hn) & (ev_rel["timestamp"] >= t0) & (ev_rel["timestamp"] <= t1)].copy()
            rel = rel.sort_values("timestamp", ascending=True)
        else:
            rel = pd.DataFrame()

        zip_bytes = build_evidence_zip_bytes(picked, rel)
        fname = f"evidence_{sel_id if sel_id else 'alert'}.zip"

        st.download_button(
            "Export evidence (ZIP)",
            data=zip_bytes,
            file_name=fname,
            mime="application/zip",
            use_container_width=False,
        )

with tab4:
    st.subheader("Endpoints")
    st.caption("Inventory derived from ingested events: hostname, last seen, channels, Sysmon presence, event rate.")

    e1, e2, e3 = st.columns([2, 2, 6])
    with e1:
        lookback = st.selectbox("Event rate window", ["24h", "6h", "72h", "168h"], index=0)
    with e2:
        sysmon_only = st.selectbox("Sysmon", ["", "present", "missing"], index=0)
    with e3:
        host_q = st.text_input("Search hostname", value="", key="endpoints_q")

    hours_map = {"6h": 6, "24h": 24, "72h": 72, "168h": 168}
    lb = hours_map.get(lookback, 24)

    eps = derive_endpoints_from_events(ev_df, lookback_hours=lb)

    if not eps.empty:
        if host_q:
            eps = eps[eps["hostname"].astype(str).str.contains(host_q, case=False, na=False)]
        if sysmon_only == "present":
            eps = eps[eps["sysmon_present"] == True]
        if sysmon_only == "missing":
            eps = eps[eps["sysmon_present"] == False]

    if eps.empty:
        st.info("No endpoints yet.")
    else:
        view = eps.copy()
        view["channels_seen"] = view["channels_seen"].apply(lambda v: ", ".join(v) if isinstance(v, list) else "")
        show_cols = ["hostname", "status", "last_seen", "sysmon_present", "event_rate", "channels_seen"]
        dark_df(view[show_cols], height_px=760)

with tab5:
    st.subheader("Rules")
    st.caption("Rule packs enforced: Auth → Persistence → Sysmon (Sysmon only if present).")

    rc = pd.DataFrame(RULES_CATALOG)
    if rc.empty:
        st.info("No rules loaded.")
    else:
        c1, c2, c3 = st.columns([2, 2, 6])
        with c1:
            pack_f = st.selectbox("Pack filter", ["", "Auth", "Persistence", "Lateral", "Sysmon"], index=0, key="rules_pack_f")
        with c2:
            sev_f = st.selectbox("Severity filter", ["", "low", "medium", "high", "high/medium", "medium/high"], index=0, key="rules_sev_f")
        with c3:
            q = st.text_input("Search", value="", key="rules_q")

        view = rc.copy()
        if pack_f:
            view = view[view["pack"] == pack_f]
        if sev_f:
            view = view[view["severity"] == sev_f]
        if q:
            qq = q.strip().lower()
            view = view[
                view.apply(
                    lambda r: any(qq in str(r.get(k, "")).lower() for k in ["pack", "rule", "severity", "signals", "default"]),
                    axis=1,
                )
            ]

        dark_df(view[["pack", "rule", "severity", "signals", "default"]], height_px=760)