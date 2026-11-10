#!/usr/bin/env python3
"""Recompute the six-county Gorge flow matrix from raw LODES8 origin-destination files.

Source: U.S. Census Bureau, LEHD Origin-Destination Employment Statistics (LODES),
version 8, job type JT00 (all jobs), column S000 (total jobs).
https://lehd.ces.census.gov/data/lodes/LODES8/

Each state publishes two OD files per year:
  main  jobs whose worker lives in the SAME state as the workplace
  aux   jobs whose worker lives in a DIFFERENT state from the workplace
A flow that crosses the Columbia River sits in the aux file of the workplace state.
Both files are read here. Nothing in either file is withheld for being cross-state.

County comes from the first five digits of the 15-digit block geocode
(2-digit state FIPS + 3-digit county FIPS). There is no crosswalk and no name join,
so an out-of-state home block cannot lose its county.

LODES counts jobs, not people. A person with two jobs is counted twice.

Standard library only. From the repo root:

  python3 scripts/recompute_flows.py --raw-dir data/raw --download

--raw-dir may be given more than once; directories are searched in order.
--download fetches any missing file from the Census server into the first --raw-dir.
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
import sys
import urllib.request
from collections import defaultdict

COUNTIES = [
    {"fips": "41027", "name": "Hood River", "state": "OR"},
    {"fips": "41065", "name": "Wasco", "state": "OR"},
    {"fips": "41051", "name": "Multnomah", "state": "OR"},
    {"fips": "53059", "name": "Skamania", "state": "WA"},
    {"fips": "53039", "name": "Klickitat", "state": "WA"},
    {"fips": "53011", "name": "Clark", "state": "WA"},
]
SIX = {c["fips"] for c in COUNTIES}
NAME = {c["fips"]: c["name"] for c in COUNTIES}
STATE_FIPS = {"or": "41", "wa": "53"}
PARTS = ("main", "aux")
URL = "https://lehd.ces.census.gov/data/lodes/LODES8/{st}/od/{name}"

# Figures audited separately for a public comment (data year 2022). The script must
# reproduce them or it stops.
ANCHORS_2022 = [
    ("flow", "53039", "41027", 753),   # Klickitat residents, Hood River workplaces
    ("flow", "53059", "41027", 343),   # Skamania residents, Hood River workplaces
    ("flow", "53011", "41027", 245),   # Clark residents, Hood River workplaces
    ("work_total", "53059", None, 2010),
    ("work_main", "53059", None, 1679),
    ("work_aux", "53059", None, 331),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def locate(name, raw_dirs, st, download):
    for d in raw_dirs:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    if not download:
        sys.exit(f"missing {name}; looked in {raw_dirs}. Re-run with --download.")
    os.makedirs(raw_dirs[0], exist_ok=True)
    p = os.path.join(raw_dirs[0], name)
    url = URL.format(st=st, name=name)
    print(f"downloading {url}")
    urllib.request.urlretrieve(url, p)
    return p


def read_file(path, st, part, flows, work, res):
    """Add one OD file to the running tallies. Returns file-level facts."""
    sf = STATE_FIPS[st]
    rows = jobs = bad = 0
    created = set()
    with gzip.open(path, "rt", newline="") as f:
        r = csv.reader(f)
        head = next(r)
        wi, hi, si, ci = (head.index(k) for k in ("w_geocode", "h_geocode", "S000", "createdate"))
        for row in r:
            w = row[wi].zfill(15)
            h = row[hi].zfill(15)
            s = int(row[si])
            rows += 1
            jobs += s
            created.add(row[ci])
            # File-definition check: workplace is always in the file's state; the home
            # is in the same state for main and in another state for aux.
            if w[:2] != sf or (h[:2] == sf) != (part == "main"):
                bad += 1
            w5, h5 = w[:5], h[:5]
            if w5 in SIX:
                work[w5][part] += s
                if h5 in SIX:
                    flows[(h5, w5)][part] += s
            if h5 in SIX:
                res[h5][part] += s
    return {"file": os.path.basename(path),
            "bytes": os.path.getsize(path), "sha256": sha256(path),
            "createdate": sorted(created), "rows": rows, "jobs_S000": jobs,
            "rows_breaking_main_aux_definition": bad}


def one_year(year, raw_dirs, download):
    flows = defaultdict(lambda: {"main": 0, "aux": 0})
    work = defaultdict(lambda: {"main": 0, "aux": 0})
    res = defaultdict(lambda: {"main": 0, "aux": 0})
    files = {}
    for st in ("or", "wa"):
        for part in PARTS:
            name = f"{st}_od_{part}_JT00_{year}.csv.gz"
            p = locate(name, raw_dirs, st, download)
            files[f"{st}_{part}"] = read_file(p, st, part, flows, work, res)
            fm = files[f"{st}_{part}"]
            print(f"  {name}: {fm['rows']:>9,} rows, {fm['jobs_S000']:>9,} jobs, createdate {fm['createdate']}")
            if fm["rows_breaking_main_aux_definition"]:
                sys.exit(f"{name}: {fm['rows_breaking_main_aux_definition']} rows break the main/aux definition")

    matrix = {}
    for hc in COUNTIES:
        h = hc["fips"]
        matrix[h] = {}
        for wc in COUNTIES:
            w = wc["fips"]
            cell = flows[(h, w)]
            matrix[h][w] = {"jobs": cell["main"] + cell["aux"], "main": cell["main"], "aux": cell["aux"]}
            # A same-state pair can only be in main; a cross-state pair only in aux.
            if hc["state"] == wc["state"]:
                assert cell["aux"] == 0, (year, h, w, cell)
            else:
                assert cell["main"] == 0, (year, h, w, cell)

    workplace, residence = {}, {}
    for c in COUNTIES:
        f = c["fips"]
        total = work[f]["main"] + work[f]["aux"]
        same = matrix[f][f]["jobs"]
        from_five = sum(matrix[h][f]["jobs"] for h in SIX if h != f)
        workplace[f] = {"name": c["name"], "jobs": total, "main": work[f]["main"], "aux": work[f]["aux"],
                        "held_by_same_county_residents": same,
                        "held_by_other_five_county_residents": from_five,
                        "held_by_residents_elsewhere": total - same - from_five}
        # Residence side: jobs at Oregon and Washington workplaces only. A resident's job
        # in a third state would be in that state's aux file, which is not read here.
        rtotal = res[f]["main"] + res[f]["aux"]
        residence[f] = {"name": c["name"], "jobs_at_or_wa_workplaces": rtotal,
                        "in_home_state": res[f]["main"], "in_other_state": res[f]["aux"],
                        "in_home_county": same, "outside_home_county": rtotal - same,
                        "pct_outside_home_county": round(100 * (rtotal - same) / rtotal, 1)}
    return {"files": files, "flows": matrix, "workplace": workplace, "residence": residence}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw-dir", action="append", required=True)
    ap.add_argument("--years", type=int, nargs="+", default=[2012, 2019, 2022])
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "flows_recomputed.json"))
    a = ap.parse_args()

    result = {"meta": {
        "publisher": "U.S. Census Bureau, Longitudinal Employer-Household Dynamics (LEHD)",
        "product": "LODES version 8, origin-destination, job type JT00 (all jobs), column S000 (total jobs)",
        "url": "https://lehd.ces.census.gov/data/lodes/LODES8/",
        "method": "main + aux for OR and WA; county = first five digits of w_geocode and h_geocode",
        "unit": "jobs (not workers)"},
        "counties": COUNTIES, "years": {}}
    for y in a.years:
        print(f"{y}")
        result["years"][str(y)] = one_year(y, a.raw_dir, a.download)

    if 2022 in a.years:
        y = result["years"]["2022"]
        print("anchor check, data year 2022")
        ok = True
        for kind, f1, f2, want in ANCHORS_2022:
            if kind == "flow":
                got, label = y["flows"][f1][f2]["jobs"], f"{NAME[f1]} residents at {NAME[f2]} workplaces"
            else:
                key = {"work_total": "jobs", "work_main": "main", "work_aux": "aux"}[kind]
                got, label = y["workplace"][f1][key], f"{NAME[f1]} workplaces, {key}"
            flag = "PASS" if got == want else "FAIL"
            ok &= got == want
            print(f"  {flag}  {label}: {got:,} (audited {want:,})")
        if not ok:
            sys.exit("anchor check failed")

    out = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
