# 📡 How I Read PCAPs (My Full Process)

> I don’t open a PCAP looking for “the exploit.”  
> I open it to **reconstruct a conversation**: who talked, about what, how often, and why.  
> When you read traffic like a story, the bad parts reveal themselves.

This is the way I triage packet captures end-to-end. It’s not a copy-paste tutorial; it’s my actual mental model — the questions I ask, the pivots I make, and the signals I trust.

---

## 🧠 Before I Click “Open”
I frame three hypotheses up front:

1) **Benign Hypothesis** — this is normal baseline: updates, browsing, chat apps.  
2) **Misconfig/Noise Hypothesis** — scanning, retries, broken clients.  
3) **Threat Hypothesis** — C2 beacons, credential abuse, staged exfil.

Everything I do will try to **support or eliminate** those hypotheses quickly.

I also clarify **scope**:
- Internal host(s) & subnets I care about
- Time window
- The question being asked: *“why is this host noisy?”* vs *“was there data theft?”*

---

## 🧭 Phase 1 — Summarize First, Packets Later (Zeek mindset)

I rarely start in Wireshark. I prefer **summaries** first — they give me shape before details.

- I run Zeek on the capture to get structured logs:
  - `conn.log` → who talked to who, how often, how big  
  - `dns.log` → questions, answers, NXDOMAIN bursts  
  - `http.log` → URIs, methods, user-agents, MIME types  
  - `ssl.log` (TLS) → SNI, ciphers, JA3/JA4, certs  
  - `files.log` → extracted files metadata (when present)

Why this matters: instead of 500k packets, I now have **readable tables** that highlight shape: fan-out, periodicity, protocols, and weirdness.

**What I look for immediately:**
- **Fan-out** (one host talking to many rare destinations)
- **Beacons** (regular intervals; similar sizes; jittered gaps)
- **Odd protocols on odd ports** (TLS on 8082, DNS on 5353 to the internet)
- **DNS behavior** (NXDOMAIN storms, random-looking subdomains, TXT abuse)
- **HTTP weird** (Base64 blobs in URIs, long query strings, uncommon user-agents)
- **TLS clues** (blank SNI, self-signed/short-lived certs, strange JA3)

If Zeek points at something, that’s where Wireshark earns its keep.

---

## 🔎 Phase 2 — Dive With Purpose (Wireshark, but focused)

Now I open the PCAP and go straight to **conversation flows** instead of raw scrolling.

### My default Wireshark pivots
- **Conversations view**: `Statistics → Conversations` (TCP/UDP tab)
  - Sort by **Packets** and **Bytes** to find dominance
  - Look for many short TCP connections to a single IP (beacon + tasking)
- **Endpoints view**: who are the talkers? Any external nets that dominate?
- **Follow Stream** on a suspicious flow for context (HTTP payloads, protocol banners)

### Filter snippets I use constantly

               - dns
               - http.request or http.response
               - tls.handshake or (tcp.port == 443 and tcp.flags.syn == 1)
               - tcp.flags.reset == 1
               - tcp.analysis.retransmission
               - tcp.stream eq X # deep-dive a single conversation
               - ip.addr == 10.0.0.15 # focus a host
               - frame.len >= 800 and ip.dst == <external> # large transfers out


**What “bad” often looks like:**
- Same-size packets leaving every ~30s (C2 beacon)
- GETs/POSTs with long, high-entropy parameters (`A-Za-z0-9+/=`)
- Repeated **404/403** with data in the request (covert channels)
- TLS with **no SNI**, uncommon ciphers, or certs with weird issuers/very short lifetimes
- DNS bursts of **random subdomains** or lots of **NXDOMAIN**
- **TXT**/**NULL** records used frequently (exfil patterns)

---

## 🧪 Phase 3 — Protocol-by-Protocol Heuristics

### DNS (fastest tell)
- **NXDOMAIN storms** → DGA or failed staging
- **Very low TTLs** → fast-flux infra
- **Random subdomain fan-out** → staging or tracking beacons
- **TXT/NULL** records** → data tunneling potential
- Pivot: resolve suspicious FQDNs; check passive DNS; look at who else asked.

**Wireshark aids:**  
`dns.flags.rcode != 0` (errors)  
`dns.qry.name contains .top or .xyz` (cheap TLDs can be noisy)

---

### HTTP / HTTPS
- **URIs** with long query strings or base64ish chunks  
- **Odd verbs** (PROPFIND/OPTIONS noise) repeatedly to non-web services  
- **User-Agents** that don’t match the OS/app  
- **Content-Type** misuse (e.g., `image/png` but body isn’t image bytes)
- **Beacon cadence**: same interval + similar size = strong signal

**TLS** (even when encrypted gives clues):
- **SNI blank** or SNI that doesn’t match dest cert  
- **JA3/JA4** fingerprints that don’t match typical browsers  
- **Self-signed** or **very short-lived** certs, weird issuers

---

### SMB / RDP / Auth
- **RDP** spikes from outside?  
- **SMB** errors/retries + big writes?  
- **Kerberos** oddities (lots of failures/ticket requests) — may pair with auth abuse.

---

## 🧵 Phase 4 — Time, Cadence, and Size (the beacon test)

I measure **intervals**:
- Are we seeing **near-exact gaps** between connections? (e.g., 30.0 ± 1.5 seconds)
- Are **payload sizes** clustered (e.g., 528–540 bytes outbound “pings”)?

Malware authors love rhythm.  
Defenders catch rhythm.

---

## 🧩 Phase 5 — Enrichment & Pivots

Once I have suspects (IPs/domains/hashes), I enrich:
- **VirusTotal** for rep/stats  
- **AbuseIPDB** for behavior  
- **Passive DNS** (where else that domain resolved)  
- **WHOIS / ASN** (hosting patterns, bulletproof hosts)

I prefer doing small batches via automation (my IOC Enricher) so I can **rank** indicators by confidence.

---

## 🧰 Phase 6 — Turning Observations into Detections

I translate the pattern into rules others can reuse:

- **SIEM query idea (Splunk):**
  ```spl
  index=network sourcetype=conn OR sourcetype=firewall
  | bin _time span=1m
  | stats count AS hits, avg(bytes_out) AS avg_sz BY src_ip, dest_ip, _time
  | streamstats window=5 avg(hits) AS avg_hits BY src_ip, dest_ip
  | where hits>0 AND avg_hits>0 AND abs(hits-avg_hits)<1 AND avg_sz<800
- **DNS beaconing ideas
  index=dns
| stats count AS q BY src_ip, query
| where q>50 AND like(query, "%.%.%.%")   /* lots of subdomain depth */

- **HTTP weird URL length
index=http method=POST
| eval urilen=len(uri_query)
| where urilen>200 AND like(uri, "%/api/%")

---

## 🧯 Phase 7 — Ruling Out False Positives

Not every spike of weird traffic is an attacker. Sometimes, it’s just Windows being Windows — or Chrome pinging ten telemetry endpoints you didn’t know existed.
When I’m investigating, I always assume I might be wrong first. It keeps me honest.

The first question I ask is: Could this be normal?
If the traffic goes to a known CDN, update server, or SaaS endpoint, that’s a good clue it’s benign.
Next, I look at timing and behavior. Some legitimate applications poll servers at fixed intervals, which can mimic beaconing — Teams, Slack, or EDR agents do this all the time.
TLS can also throw people off; SNI fields can be blank in modern SASE or proxy setups, and that doesn’t mean it’s malicious.

The real challenge is context. Is this an isolated host or part of a pattern?
If multiple endpoints show similar traffic, I start thinking configuration issue or a vendor behavior.
If it’s just one machine acting different — that’s when the hair on the back of my neck goes up.

The truth is, most of your job as an analyst isn’t finding evil — it’s proving normal.
Anyone can flag anomalies, but the skill lies in knowing when not to panic.
False positives teach you just as much about your environment as true detections do.

---

## 📸 What I Capture (for Reports)

When I finish an analysis, I document it like I’m explaining it to someone who wasn’t there.
I don’t just throw logs at them — I tell the story visually and logically.

I start with a conversation overview — a screenshot of the network summary showing who talked to whom and how much. That gives context.
Then I grab the Wireshark stream view of the suspicious flow — seeing the headers, timing, and payloads side-by-side tells more than a thousand words.

If DNS was in play, I’ll show a timeline of queries, especially if there’s NXDOMAIN noise or random subdomains. For TLS cases, I include certificate details, JA3 fingerprints, or SNI anomalies.

Finally, I write a short narrative:

“At 14:03 UTC, the host initiated outbound connections to random subdomains on port 443. TLS handshakes used an uncommon cipher suite and self-signed certs. Behavior consistent with C2 beaconing.”

The goal isn’t to impress anyone — it’s to make it reproducible.
Anyone reading the report should be able to follow your logic, recreate your findings, and reach the same conclusion.

---

## 🧱 My Mental Checklist

Every time I open a PCAP, there’s a quiet little checklist running in my head.
I don’t write it down anymore — it’s muscle memory — but it’s always there guiding me.

I start by asking: Who are the talkers? Internal? External? Cloud?
Then: Is there rhythm in the traffic? Beacons love rhythm. Humans don’t.

I scan for odd protocols or mismatched ports — HTTP on 4443, DNS on 8080, things that shouldn’t be there.
Then I move to DNS behavior: random subdomains, TXT records, or an endless list of NXDOMAINs can tell me a lot about what’s trying to call home.

With HTTP traffic, I’m watching URI lengths, encoded payloads, and strange user agents that don’t belong on workstations.
TLS has its own language — blank SNI fields, weird certificate issuers, and uncommon JA3 hashes all whisper little clues about what’s hiding behind encryption.

If I see data going out in a steady pattern, small bursts, or unusual timing, I start thinking exfil or beaconing.
Then I enrich — VirusTotal, AbuseIPDB, WHOIS — to validate my gut feeling.
And if something stands out enough that I could explain it to a colleague and they’d nod instead of squint, I know I’ve probably found something real.

When all that’s done, I ask myself the most important question:

“Can I turn this observation into a detection rule that helps the next analyst catch it faster?”

That’s the difference between analyzing and defending.
One finds threats; the other builds systems that don’t miss them again.
