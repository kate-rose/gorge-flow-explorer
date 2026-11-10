# Columbia River Gorge Commuter Flow Explorer

An interactive tool for exploring origin-destination commute flows between counties in the Columbia River Gorge region, built from U.S. Census Bureau LEHD data.

## What this is

This tool maps the specific bidirectional flow of workers between any two Gorge-area counties across three years: 2012, 2019, and 2022. It was built to support reporting and policy work on housing displacement and workforce economics in Hood River, Wasco, Klickitat, and Skamania counties, with Clark and Multnomah available for regional context.

The core question it tries to answer: are the people who work in a given county able to live there, and has that changed over time?

## Data source

All figures come from the U.S. Census Bureau's **LEHD Origin-Destination Employment Statistics, Version 8 (LODES8)**, a dataset derived from state unemployment insurance records and federal employment data compiled through the Local Employment Dynamics (LED) Partnership.

Specifically, this tool uses:
- **OD main files** — jobs where both workplace and residence are within the same state
- **OD aux files** — jobs where workplace and residence are in different states
- **Job type: JT00** (All Jobs)

Raw files were downloaded directly from:
```
https://lehd.ces.census.gov/data/lodes/LODES8/{state}/od/
```

## Why these three years

**2012** — Post-recession baseline. The Gorge economy was still recovering, housing costs had not yet accelerated, and this gives a clean pre-displacement starting point.

**2019** — Pre-COVID peak. Captures the full effect of the 2010s housing run-up before pandemic disruptions to commute patterns.

**2022** — Most recent available LODES8 data at time of analysis. Reflects post-COVID settlement of both housing markets and work patterns.

## Why Clark and Multnomah are excluded from primary analysis

Clark (WA) and Multnomah (OR) are included in the tool as selectable counties but were excluded from the primary displacement analysis for two reasons.

First, scale. Clark County has roughly 120,000 local jobs and Multnomah over 240,000 — an order of magnitude larger than the core Gorge counties. Including them in aggregate comparisons visually and statistically overwhelms the signal from Hood River, Wasco, Klickitat, and Skamania, making county-level trends illegible.

Second, labor market dynamics. Clark and Multnomah are urban counties anchored to the Portland metropolitan area. Their commute patterns are shaped by metro-scale forces — regional transit infrastructure, urban housing markets, large employer concentrations — that are categorically different from the rural Gorge counties this analysis focuses on. Displacement pressure in Hood River or Skamania reflects the specific constraints of a small, geographically isolated labor market inside a nationally designated scenic area with significant land use restrictions. That is a different phenomenon than suburbanization or urban housing spillover, and mixing them muddies the analysis.

Researchers interested in the Clark-Multnomah corridor specifically should treat that as a separate inquiry. Both counties are available in the tool for reference and comparison.

## Known limitations

**Jobs, not people.** LODES counts job-holding instances. A worker with two jobs appears in the data twice. This inflates raw counts slightly but does not meaningfully affect directional trends or county-pair comparisons.

**Undercounted workers.** Self-employed workers, most agricultural workers, and gig economy workers are not well represented in unemployment insurance records. In rural counties like Hood River and Wasco, where agriculture is a significant employer, this is a non-trivial gap. Treat absolute job counts as conservative floor estimates rather than complete tallies.

**Cross-state flows.** A flow between an Oregon county and a Washington county comes from the LODES aux file of the state where the job is. An aux file holds the jobs at that state's workplaces whose holder lives in another state. The main file holds only same-state pairs. This tool reads both. Nothing is withheld for being cross-state.

**Correction.** The first version of this tool (May 2026) showed every flow between an Oregon Gorge county and a Washington Gorge county as zero and said a federal disclosure threshold was the reason. That was wrong. The cause was in the merge. County names were joined from each state's own crosswalk, so an out-of-state home block got no county name and dropped out of the county totals. The scripts now take the county from the first five digits of each block geocode. In a full recheck against the raw files, 74 of the tool's 90 figures changed. `data/audit_may2026_page.csv` lists every one.

**Geography is current, not historical.** The LODES8 crosswalk uses 2020 Census block boundaries. County boundaries in this region have not changed, so this does not affect the analysis, but researchers combining this data with older shapefiles should verify alignment.

**2022 remote work effects.** Post-COVID remote and hybrid work patterns may affect what 2022 commute data captures relative to prior years. Some workers recorded as commuting to a county in 2019 may have shifted to remote arrangements by 2022, which could suppress apparent commute flows independent of housing or employment changes.

## How to replicate

Three scripts in `scripts/` rebuild every number in the tool. They use only the Python standard library.

1. `python3 scripts/recompute_flows.py --raw-dir data/raw --download` fetches the OD main and aux files for Oregon and Washington (JT00; 2012, 2019, 2022) and writes `data/flows_recomputed.json`.
2. `python3 scripts/compare_to_page.py` checks every cell of the page's FLOWS table against that file and writes `data/comparison.csv`. The saved check of the May 2026 page is `data/audit_may2026_page.csv`.
3. `python3 scripts/framing_check.py` writes county job totals and flow rankings to `data/framing_check.md`.

County is the first five digits of `w_geocode` (workplace block) and `h_geocode` (home block). No crosswalk is needed.

## County FIPS reference

| County | State | FIPS |
|---|---|---|
| Hood River | OR | 41027 |
| Wasco | OR | 41065 |
| Klickitat | WA | 53039 |
| Skamania | WA | 53059 |
| Clark | WA | 53011 |
| Multnomah | OR | 41051 |

## Citation

U.S. Census Bureau, LEHD Origin-Destination Employment Statistics (LODES8, v8.3), All Jobs (JT00), 2012, 2019, 2022. https://lehd.ces.census.gov/data/lodes/LODES8/

Analysis and tool by **Open Gorge** / Skamania Dispatch. Published May 2026.
