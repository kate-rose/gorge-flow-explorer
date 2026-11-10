#!/usr/bin/env python3
"""Numbers behind two sentences in the page copy at opengorge.org/gorge-commuter-flows:

  "In the Gorge, the job base has been relatively stable."
  "Start with Wasco as home and Hood River as work - that's the Gorge's clearest
   on-the-ground displacement pattern."

Reads data/flows_recomputed.json (made by recompute_flows.py). Writes data/framing_check.md.
All figures are jobs, LODES8, JT00, S000, main + aux, data years 2012, 2019, 2022.
LODES records where a job is and where its holder lives in a given year. It does not
record whether anyone moved, or why.

Standard library only. From the repo root:  python3 scripts/framing_check.py
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
d = json.load(open(os.path.join(ROOT, "data", "flows_recomputed.json")))
Y = ["2012", "2019", "2022"]
NAME = {c["fips"]: c["name"] for c in d["counties"]}
GORGE = ["41027", "41065", "53039", "53059"]
ALL = ["41027", "41065", "53039", "53059", "53011", "41051"]


def flow(y, h, w):
    return d["years"][y]["flows"][h][w]["jobs"]


def pct(a, b):
    return f"{100 * (b - a) / a:+.1f}%"


out = []
P = out.append
P("# Framing check")
P("")
P("Source: U.S. Census Bureau, LEHD, LODES version 8, origin-destination files (main + aux, Oregon and")
P("Washington), job type JT00, column S000. Data years 2012, 2019, 2022. All figures are jobs.")
P("Made by `scripts/framing_check.py`.")
P("")

P("## 1. Jobs at workplaces in each county")
P("")
P("| County | 2012 | 2019 | 2022 | 2012 to 2019 | 2019 to 2022 | 2012 to 2022 | Jobs added or lost, 2012 to 2022 |")
P("|---|--:|--:|--:|--:|--:|--:|--:|")
tot = {y: 0 for y in Y}
for f in GORGE:
    v = [d["years"][y]["workplace"][f]["jobs"] for y in Y]
    for y, x in zip(Y, v):
        tot[y] += x
    P(f"| {NAME[f]} | {v[0]:,} | {v[1]:,} | {v[2]:,} | {pct(v[0], v[1])} | {pct(v[1], v[2])} | {pct(v[0], v[2])} | {v[2] - v[0]:+,} |")
v = [tot[y] for y in Y]
P(f"| Four Gorge counties | {v[0]:,} | {v[1]:,} | {v[2]:,} | {pct(v[0], v[1])} | {pct(v[1], v[2])} | {pct(v[0], v[2])} | {v[2] - v[0]:+,} |")
P("")

P("## 2. Every flow between two of the four Gorge counties, largest first (2022)")
P("")
P("| Home → Work | Crosses the river | 2012 | 2019 | 2022 | Change in jobs, 2012 to 2022 | Percent |")
P("|---|---|--:|--:|--:|--:|--:|")
pairs = [(h, w) for h in GORGE for w in GORGE if h != w]
pairs.sort(key=lambda p: -flow("2022", *p))
for h, w in pairs:
    v = [flow(y, h, w) for y in Y]
    cross = "yes" if h[:2] != w[:2] else "no"
    P(f"| {NAME[h]} → {NAME[w]} | {cross} | {v[0]:,} | {v[1]:,} | {v[2]:,} | {v[2] - v[0]:+,} | {pct(v[0], v[2])} |")
P("")

P("## 3. Net flow for each pair of Gorge counties")
P("")
P("Net = jobs held in the second county by residents of the first, minus the reverse.")
P("")
P("| Pair | Crosses the river | 2012 net | 2019 net | 2022 net |")
P("|---|---|--:|--:|--:|")
seen = set()
for h, w in pairs:
    if (w, h) in seen:
        continue
    seen.add((h, w))
    n = [flow(y, h, w) - flow(y, w, h) for y in Y]
    cross = "yes" if h[:2] != w[:2] else "no"
    P(f"| {NAME[h]} → {NAME[w]} minus reverse | {cross} | {n[0]:+,} | {n[1]:+,} | {n[2]:+,} |")
P("")

P("## 4. Who holds the jobs at Hood River County workplaces")
P("")
P("| Home of job holder | 2012 jobs | 2012 share | 2019 jobs | 2019 share | 2022 jobs | 2022 share | Change in jobs, 2012 to 2022 |")
P("|---|--:|--:|--:|--:|--:|--:|--:|")
HR = "41027"
tots = {y: d["years"][y]["workplace"][HR]["jobs"] for y in Y}
rows = [(NAME[h], [flow(y, h, HR) for y in Y]) for h in [HR, "41065", "53039", "53059", "41051", "53011"]]
wa_gorge = [flow(y, "53039", HR) + flow(y, "53059", HR) for y in Y]
rows.insert(4, ("Klickitat + Skamania together", wa_gorge))
rows.append(("Everywhere else", [d["years"][y]["workplace"][HR]["held_by_residents_elsewhere"] for y in Y]))
rows.append(("All jobs at Hood River workplaces", [tots[y] for y in Y]))
for name, v in rows:
    cells = " | ".join(f"{x:,} | {100 * x / tots[y]:.1f}%" for x, y in zip(v, Y))
    P(f"| {name} | {cells} | {v[2] - v[0]:+,} |")
P("")

P("## 5. Jobs held by each Gorge county's residents (Oregon and Washington workplaces)")
P("")
P("A job in a third state would be in that state's aux file, which was not read.")
P("")
P("| Home county | Year | Jobs held by residents | In home county | Outside home county | Share outside | In the other state |")
P("|---|---|--:|--:|--:|--:|--:|")
for f in GORGE:
    for y in Y:
        r = d["years"][y]["residence"][f]
        P(f"| {NAME[f]} | {y} | {r['jobs_at_or_wa_workplaces']:,} | {r['in_home_county']:,} | {r['outside_home_county']:,} | {r['pct_outside_home_county']}% | {r['in_other_state']:,} |")
P("")

open(os.path.join(ROOT, "data", "framing_check.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
