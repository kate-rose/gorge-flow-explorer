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
- **Geographic crosswalk files** — linking Census block IDs to county FIPS codes
- **Job type: JT00** (All Jobs)

Raw files were downloaded directly from:
```
https://lehd.ces.census.gov/data/lodes/LODES8/{state}/od/
https://lehd.ces.census.gov/data/lodes/LODES8/{state}/{state}_xwalk.csv.gz
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

**Cross-state flows between Gorge counties.** Direct flows between Oregon Gorge counties (Hood River, Wasco) and Washington Gorge counties (Klickitat, Skamania) show as zero in this dataset. This reflects LODES disclosure avoidance thresholds applied to small cross-state flows — not an absence of cross-river commuting. The aux files capture out-of-state workers but require the home state to report them; small flows are suppressed. Anyone needing precise cross-river flow data should consider supplementing with ACS journey-to-work tables or state DOT commute surveys.

**Geography is current, not historical.** The LODES8 crosswalk uses 2020 Census block boundaries. County boundaries in this region have not changed, so this does not affect the analysis, but researchers combining this data with older shapefiles should verify alignment.

**2022 remote work effects.** Post-COVID remote and hybrid work patterns may affect what 2022 commute data captures relative to prior years. Some workers recorded as commuting to a county in 2019 may have shifted to remote arrangements by 2022, which could suppress apparent commute flows independent of housing or employment changes.

## How to replicate

The analysis was built in Python using pandas. The full download and merge script is available in this repository as `gorge_flow_explorer.html` — a self-contained HTML file requiring no server or dependencies to run locally.

To replicate the underlying data pipeline:

1. Download OD main and aux files for Oregon and Washington from the LODES8 directory above
2. Download the geographic crosswalk for each state
3. Merge OD files to crosswalk on `w_geocode` (workplace Census block) and `h_geocode` (home Census block) to attach county FIPS codes
4. Filter to county pairs of interest
5. Group by `h_cty` / `w_cty` and sum `S000` (total jobs) for each year

**Note:** The crosswalk column for county FIPS in LODES8 is `cty` — not `stcofips` as documented in some older LODES versions. This discrepancy will cause a silent merge failure if you are working from older documentation.

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
