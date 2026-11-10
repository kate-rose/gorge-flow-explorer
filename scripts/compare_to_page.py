#!/usr/bin/env python3
"""Compare every cell of the page's FLOWS table with the recomputed LODES8 value.

Reads the `const FLOWS` and `const SKAMANIA_FISCAL` blocks out of gorge_flow_explorer.html
and data/flows_recomputed.json (made by recompute_flows.py). Writes:

  data/comparison.csv        one row per cell per year (30 pairs x 3 years = 90 rows)
  data/comparison.md         the same as readable tables, plus county job totals
  data/proposed_FLOWS.js     the corrected FLOWS and SKAMANIA_FISCAL blocks, ready to paste

Standard library only. From the repo root:

  python3 scripts/compare_to_page.py [page.html] [--out-prefix data/comparison]

data/audit_may2026_page.csv and .md are the saved check of the first published version
of the page (commit 86a78ff, May 2026). To remake them:

  git show 86a78ff:gorge_flow_explorer.html > /tmp/may2026.html
  python3 scripts/compare_to_page.py /tmp/may2026.html --out-prefix data/audit_may2026_page
"""
import argparse
import csv
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ap = argparse.ArgumentParser()
ap.add_argument("html", nargs="?", default=os.path.join(ROOT, "gorge_flow_explorer.html"))
ap.add_argument("--out-prefix", default=os.path.join(ROOT, "data", "comparison"))
args = ap.parse_args()
HTML, PREFIX = args.html, args.out_prefix
RECOMP = os.path.join(ROOT, "data", "flows_recomputed.json")
YEARS = ["2012", "2019", "2022"]
# Order used on the page (home blocks, then work rows inside each).
PAGE_ORDER = ["41065", "41027", "53039", "53059", "53011", "41051"]
WORK_ORDER = ["41027", "41065", "53039", "53059", "53011", "41051"]

data = json.load(open(RECOMP))
NAME = {c["fips"]: c["name"] for c in data["counties"]}
STATE = {c["fips"]: c["state"] for c in data["counties"]}
src = open(HTML, encoding="utf-8").read()


def parse_flows(text):
    block = re.search(r"const FLOWS = \{(.*?)\n\};", text, re.S).group(1)
    page, home = {}, None
    for line in block.splitlines():
        m = re.match(r'\s*"(\d{5})": \{ // .* home', line)
        if m:
            home = m.group(1)
            page[home] = {}
            continue
        m = re.match(r'\s*"(\d{5})": \{ 2012:\s*(\d+), 2019:\s*(\d+), 2022:\s*(\d+) \},\s*//\s*(.*)', line)
        if m:
            work, a, b, c, comment = m.groups()
            page[home][work] = {"2012": int(a), "2019": int(b), "2022": int(c), "comment": comment.strip()}
    return page


def label_of(comment):
    if "below threshold" in comment:
        return "zero, 'below threshold'"
    if "CONFIRMED" in comment:
        return "CONFIRMED"
    if "from summary" in comment:
        return "from summary"
    if "estimate" in comment:
        return "estimate"
    return "no label"


page = parse_flows(src)
n_cells = sum(len(v) for v in page.values())
assert n_cells == 30, f"expected 30 home-work pairs on the page, parsed {n_cells}"

rows = []
for h in PAGE_ORDER:
    for w in WORK_ORDER:
        if h == w:
            continue
        p = page[h][w]
        for y in YEARS:
            new = data["years"][y]["flows"][h][w]
            rows.append({
                "home_fips": h, "home": NAME[h], "work_fips": w, "work": NAME[w],
                "pair_type": "same-state" if STATE[h] == STATE[w] else "cross-state",
                "page_label": label_of(p["comment"]), "year": y,
                "page_value": p[y], "recomputed_jobs": new["jobs"],
                "from_main": new["main"], "from_aux": new["aux"],
                "difference": new["jobs"] - p[y],
                "match": "yes" if new["jobs"] == p[y] else "no",
            })

with open(PREFIX + ".csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader()
    wr.writerows(rows)

# ---- readable report -------------------------------------------------------------
out = []
P = out.append
P("# Page FLOWS table versus recomputed LODES8 values")
P("")
P("Source: U.S. Census Bureau, LEHD, LODES version 8, origin-destination files, job type JT00,")
P("column S000 (total jobs), main + aux for Oregon and Washington. Data years 2012, 2019, 2022.")
P("County = first five digits of the block geocode. All figures are jobs. Made by")
P("`scripts/compare_to_page.py` from `data/flows_recomputed.json`.")
P("")
P("Raw files read:")
P("")
P("| Data year | File | LODES createdate | Rows | Jobs (S000) | sha256 (first 12) |")
P("|---|---|---|--:|--:|---|")
for y in YEARS:
    for k in ("or_main", "or_aux", "wa_main", "wa_aux"):
        fm = data["years"][y]["files"][k]
        P(f"| {y} | {fm['file']} | {', '.join(fm['createdate'])} | {fm['rows']:,} | {fm['jobs_S000']:,} | {fm['sha256'][:12]} |")
P("")

tot = len(rows)
hit = sum(r["match"] == "yes" for r in rows)
P(f"Values compared: {tot} (30 home-work pairs x 3 years). Exact matches: {hit}. Mismatches: {tot - hit}.")
P("")
for ptype in ("same-state", "cross-state"):
    sub = [r for r in rows if r["pair_type"] == ptype]
    P(f"- {ptype}: {len(sub)} values, {sum(r['match'] == 'yes' for r in sub)} match, {sum(r['match'] == 'no' for r in sub)} do not")
P("")
P("By the label the page's code comment gives the cell:")
P("")
P("| Page label | Pairs | Values | Match | Do not match |")
P("|---|--:|--:|--:|--:|")
for lab in ("CONFIRMED", "from summary", "estimate", "no label", "zero, 'below threshold'"):
    sub = [r for r in rows if r["page_label"] == lab]
    P(f"| {lab} | {len(sub) // 3} | {len(sub)} | {sum(r['match'] == 'yes' for r in sub)} | {sum(r['match'] == 'no' for r in sub)} |")
P("")

for ptype, title in (("same-state", "Same-state pairs (LODES main files)"),
                     ("cross-state", "Cross-state pairs (LODES aux files)")):
    P(f"## {title}")
    P("")
    P("| Home → Work | Page label | 2012 page | 2012 LODES | 2019 page | 2019 LODES | 2022 page | 2022 LODES | Years matching |")
    P("|---|---|--:|--:|--:|--:|--:|--:|---|")
    for h in PAGE_ORDER:
        for w in WORK_ORDER:
            sub = [r for r in rows if r["home_fips"] == h and r["work_fips"] == w and r["pair_type"] == ptype]
            if not sub:
                continue
            cells = " | ".join(f"{r['page_value']:,} | {r['recomputed_jobs']:,}" for r in sub)
            ok = [r["year"] for r in sub if r["match"] == "yes"]
            P(f"| {NAME[h]} → {NAME[w]} | {sub[0]['page_label']} | {cells} | {', '.join(ok) if ok else 'none'} |")
    P("")

# ---- county totals ---------------------------------------------------------------
P("## Jobs at workplaces in each county (main + aux)")
P("")
P("| County | 2012 | 2019 | 2022 | Change 2012 to 2022 | 2022 from aux (worker lives in another state) |")
P("|---|--:|--:|--:|--:|--:|")
four = {y: 0 for y in YEARS}
for f in ["41027", "41065", "53039", "53059", "53011", "41051"]:
    v = {y: data["years"][y]["workplace"][f] for y in YEARS}
    if f in ("41027", "41065", "53039", "53059"):
        for y in YEARS:
            four[y] += v[y]["jobs"]
    ch = 100 * (v["2022"]["jobs"] - v["2012"]["jobs"]) / v["2012"]["jobs"]
    P(f"| {NAME[f]} | {v['2012']['jobs']:,} | {v['2019']['jobs']:,} | {v['2022']['jobs']:,} | {ch:+.1f}% | {v['2022']['aux']:,} |")
ch = 100 * (four["2022"] - four["2012"]) / four["2012"]
P(f"| Four Gorge counties | {four['2012']:,} | {four['2019']:,} | {four['2022']:,} | {ch:+.1f}% | |")
P("")

# ---- Skamania box ----------------------------------------------------------------
fiscal = {}
for m in re.finditer(r"(\d{4}): \{ total: (\d+), local: (\d+), out: (\d+), pctOut: ([\d.]+), totalJobs: (\d+) \}", src):
    fiscal[m.group(1)] = {"total": int(m.group(2)), "local": int(m.group(3)), "out": int(m.group(4)),
                          "pctOut": float(m.group(5)), "totalJobs": int(m.group(6))}
P("## Skamania box (`SKAMANIA_FISCAL`)")
P("")
P("Residence-side figures count jobs at Oregon and Washington workplaces held by Skamania residents.")
P("A job in a third state would be in that state's aux file, which was not read.")
P("")
P("| Year | Field | Page | LODES main + aux | Of which main (WA workplaces) | Of which aux (OR workplaces) |")
P("|---|---|--:|--:|--:|--:|")
for y in YEARS:
    r = data["years"][y]["residence"]["53059"]
    wk = data["years"][y]["workplace"]["53059"]
    pg = fiscal[y]
    P(f"| {y} | jobs held by Skamania residents | {pg['total']:,} | {r['jobs_at_or_wa_workplaces']:,} | {r['in_home_state']:,} | {r['in_other_state']:,} |")
    P(f"| {y} | of those, at Skamania workplaces | {pg['local']:,} | {r['in_home_county']:,} | | |")
    P(f"| {y} | of those, outside Skamania | {pg['out']:,} | {r['outside_home_county']:,} | | |")
    P(f"| {y} | share outside Skamania | {pg['pctOut']}% | {r['pct_outside_home_county']}% | | |")
    P(f"| {y} | jobs at Skamania workplaces | {pg['totalJobs']:,} | {wk['jobs']:,} | {wk['main']:,} | {wk['aux']:,} |")
P("")
open(PREFIX + ".md", "w").write("\n".join(out) + "\n")

# ---- proposed blocks -------------------------------------------------------------
js = []
J = js.append
J("// ── Flow data from raw LODES8 origin-destination files ───────────────────────")
J("// FLOWS[home_fips][work_fips] = {2012, 2019, 2022}, in jobs (S000, job type JT00).")
J("// Every value is computed by scripts/recompute_flows.py from the Census Bureau's")
J("// main AND aux files for Oregon and Washington. Same-state pairs come from main.")
J("// Cross-state pairs come from aux. County = first five digits of the block geocode.")
J("const FLOWS = {")
for h in PAGE_ORDER:
    J(f'  "{h}": {{ // {NAME[h]} home')
    for w in page[h]:
        v = [data["years"][y]["flows"][h][w]["jobs"] for y in YEARS]
        part = "main" if STATE[h] == STATE[w] else "aux"
        J(f'    "{w}": {{ 2012: {v[0]:>5}, 2019: {v[1]:>5}, 2022: {v[2]:>5} }}, // → {NAME[w]} ({part})')
    J("  },")
J("};")
J("")
J("// ── Skamania residence and workplace totals (same script) ────────────────────")
J("// total = jobs at Oregon and Washington workplaces held by Skamania residents.")
J("const SKAMANIA_FISCAL = {")
for y in YEARS:
    r = data["years"][y]["residence"]["53059"]
    wk = data["years"][y]["workplace"]["53059"]
    J(f"  {y}: {{ total: {r['jobs_at_or_wa_workplaces']}, local: {r['in_home_county']}, out: {r['outside_home_county']}, "
      f"pctOut: {r['pct_outside_home_county']}, totalJobs: {wk['jobs']} }},")
J("};")
open(os.path.join(ROOT, "data", "proposed_FLOWS.js"), "w").write("\n".join(js) + "\n")

print("\n".join(out))
