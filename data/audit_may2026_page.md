# Page FLOWS table versus recomputed LODES8 values

Source: U.S. Census Bureau, LEHD, LODES version 8, origin-destination files, job type JT00,
column S000 (total jobs), main + aux for Oregon and Washington. Data years 2012, 2019, 2022.
County = first five digits of the block geocode. All figures are jobs. Made by
`scripts/compare_to_page.py` from `data/flows_recomputed.json`.

Raw files read:

| Data year | File | LODES createdate | Rows | Jobs (S000) | sha256 (first 12) |
|---|---|---|--:|--:|---|
| 2012 | or_od_main_JT00_2012.csv.gz | 20230321 | 1,382,835 | 1,515,702 | d865fd1aa55c |
| 2012 | or_od_aux_JT00_2012.csv.gz | 20230321 | 106,349 | 109,891 | 432f794a3b2a |
| 2012 | wa_od_main_JT00_2012.csv.gz | 20230321 | 2,380,603 | 2,734,050 | b41cdd99c1d1 |
| 2012 | wa_od_aux_JT00_2012.csv.gz | 20230321 | 74,514 | 76,570 | c1bc27daee06 |
| 2019 | or_od_main_JT00_2019.csv.gz | 20230321 | 1,641,252 | 1,808,573 | ec0635853100 |
| 2019 | or_od_aux_JT00_2019.csv.gz | 20230321 | 130,690 | 134,304 | 740ec142f509 |
| 2019 | wa_od_main_JT00_2019.csv.gz | 20230321 | 2,801,847 | 3,177,560 | a5bbc04a735f |
| 2019 | wa_od_aux_JT00_2019.csv.gz | 20230321 | 103,021 | 105,414 | 97f180c9da0b |
| 2022 | or_od_main_JT00_2022.csv.gz | 20240920 | 1,644,265 | 1,798,168 | 632d33220d69 |
| 2022 | or_od_aux_JT00_2022.csv.gz | 20240920 | 128,598 | 132,230 | 4f5771cfefeb |
| 2022 | wa_od_main_JT00_2022.csv.gz | 20240920 | 2,905,296 | 3,322,901 | f84c7262731c |
| 2022 | wa_od_aux_JT00_2022.csv.gz | 20240920 | 109,725 | 112,080 | 7cfc213f6cca |

Values compared: 90 (30 home-work pairs x 3 years). Exact matches: 16. Mismatches: 74.

- same-state: 36 values, 16 match, 20 do not
- cross-state: 54 values, 0 match, 54 do not

By the label the page's code comment gives the cell:

| Page label | Pairs | Values | Match | Do not match |
|---|--:|--:|--:|--:|
| CONFIRMED | 11 | 33 | 15 | 18 |
| from summary | 6 | 18 | 1 | 17 |
| estimate | 2 | 6 | 0 | 6 |
| no label | 3 | 9 | 0 | 9 |
| zero, 'below threshold' | 8 | 24 | 0 | 24 |

## Same-state pairs (LODES main files)

| Home → Work | Page label | 2012 page | 2012 LODES | 2019 page | 2019 LODES | 2022 page | 2022 LODES | Years matching |
|---|---|--:|--:|--:|--:|--:|--:|---|
| Wasco → Hood River | CONFIRMED | 1,080 | 1,080 | 1,422 | 1,422 | 1,430 | 1,430 | 2012, 2019, 2022 |
| Wasco → Multnomah | CONFIRMED | 880 | 1,109 | 960 | 966 | 1,037 | 1,037 | 2022 |
| Hood River → Wasco | CONFIRMED | 737 | 737 | 734 | 734 | 758 | 758 | 2012, 2019, 2022 |
| Hood River → Multnomah | CONFIRMED | 780 | 764 | 870 | 768 | 929 | 929 | 2022 |
| Klickitat → Skamania | from summary | 90 | 352 | 95 | 97 | 101 | 101 | 2022 |
| Klickitat → Clark | CONFIRMED | 310 | 694 | 340 | 232 | 365 | 365 | 2022 |
| Skamania → Klickitat | CONFIRMED | 332 | 424 | 289 | 386 | 332 | 332 | 2022 |
| Skamania → Clark | CONFIRMED | 921 | 1,030 | 802 | 954 | 1,068 | 1,068 | 2022 |
| Clark → Klickitat | CONFIRMED | 310 | 294 | 350 | 426 | 397 | 397 | 2022 |
| Clark → Skamania | CONFIRMED | 260 | 273 | 290 | 298 | 328 | 328 | 2022 |
| Multnomah → Hood River | CONFIRMED | 520 | 380 | 580 | 758 | 645 | 645 | 2022 |
| Multnomah → Wasco | CONFIRMED | 280 | 282 | 310 | 285 | 349 | 349 | 2022 |

## Cross-state pairs (LODES aux files)

| Home → Work | Page label | 2012 page | 2012 LODES | 2019 page | 2019 LODES | 2022 page | 2022 LODES | Years matching |
|---|---|--:|--:|--:|--:|--:|--:|---|
| Wasco → Klickitat | zero, 'below threshold' | 0 | 294 | 0 | 429 | 0 | 413 | none |
| Wasco → Skamania | zero, 'below threshold' | 0 | 23 | 0 | 10 | 0 | 36 | none |
| Wasco → Clark | no label | 28 | 64 | 34 | 69 | 40 | 80 | none |
| Hood River → Klickitat | zero, 'below threshold' | 0 | 388 | 0 | 570 | 0 | 428 | none |
| Hood River → Skamania | zero, 'below threshold' | 0 | 73 | 0 | 83 | 0 | 81 | none |
| Hood River → Clark | no label | 30 | 55 | 38 | 56 | 44 | 73 | none |
| Klickitat → Hood River | zero, 'below threshold' | 0 | 719 | 0 | 769 | 0 | 753 | none |
| Klickitat → Wasco | zero, 'below threshold' | 0 | 478 | 0 | 553 | 0 | 507 | none |
| Klickitat → Multnomah | from summary | 163 | 514 | 185 | 406 | 163 | 588 | none |
| Skamania → Hood River | zero, 'below threshold' | 0 | 321 | 0 | 383 | 0 | 343 | none |
| Skamania → Wasco | zero, 'below threshold' | 0 | 86 | 0 | 60 | 0 | 60 | none |
| Skamania → Multnomah | no label | 16 | 681 | 20 | 662 | 24 | 660 | none |
| Clark → Hood River | from summary | 180 | 170 | 210 | 229 | 255 | 245 | none |
| Clark → Wasco | from summary | 90 | 123 | 105 | 110 | 134 | 107 | none |
| Clark → Multnomah | estimate | 8,200 | 44,052 | 9,200 | 49,818 | 9,500 | 44,936 | none |
| Multnomah → Klickitat | from summary | 120 | 103 | 140 | 90 | 163 | 115 | none |
| Multnomah → Skamania | from summary | 16 | 55 | 20 | 64 | 24 | 88 | none |
| Multnomah → Clark | estimate | 3,200 | 8,814 | 3,800 | 11,407 | 3,900 | 10,946 | none |

## Jobs at workplaces in each county (main + aux)

| County | 2012 | 2019 | 2022 | Change 2012 to 2022 | 2022 from aux (worker lives in another state) |
|---|--:|--:|--:|--:|--:|
| Hood River | 11,203 | 13,625 | 13,335 | +19.0% | 2,184 |
| Wasco | 9,243 | 10,027 | 9,924 | +7.4% | 1,257 |
| Klickitat | 6,364 | 7,127 | 6,972 | +9.6% | 1,434 |
| Skamania | 2,264 | 2,210 | 2,010 | -11.2% | 331 |
| Clark | 126,380 | 162,390 | 176,192 | +39.4% | 21,476 |
| Multnomah | 451,445 | 533,622 | 512,868 | +13.6% | 58,903 |
| Four Gorge counties | 29,074 | 32,989 | 32,241 | +10.9% | |

## Skamania box (`SKAMANIA_FISCAL`)

Residence-side figures count jobs at Oregon and Washington workplaces held by Skamania residents.
A job in a third state would be in that state's aux file, which was not read.

| Year | Field | Page | LODES main + aux | Of which main (WA workplaces) | Of which aux (OR workplaces) |
|---|---|--:|--:|--:|--:|
| 2012 | jobs held by Skamania residents | 3,626 | 5,410 | 3,626 | 1,784 |
| 2012 | of those, at Skamania workplaces | 1,101 | 1,101 | | |
| 2012 | of those, outside Skamania | 2,525 | 4,309 | | |
| 2012 | share outside Skamania | 69.6% | 79.6% | | |
| 2012 | jobs at Skamania workplaces | 2,264 | 2,264 | 1,974 | 290 |
| 2019 | jobs held by Skamania residents | 3,709 | 5,618 | 3,709 | 1,909 |
| 2019 | of those, at Skamania workplaces | 1,253 | 1,253 | | |
| 2019 | of those, outside Skamania | 2,456 | 4,365 | | |
| 2019 | share outside Skamania | 66.2% | 77.7% | | |
| 2019 | jobs at Skamania workplaces | 2,210 | 2,210 | 1,901 | 309 |
| 2022 | jobs held by Skamania residents | 3,821 | 5,698 | 3,821 | 1,877 |
| 2022 | of those, at Skamania workplaces | 1,106 | 1,106 | | |
| 2022 | of those, outside Skamania | 2,715 | 4,592 | | |
| 2022 | share outside Skamania | 71.1% | 80.6% | | |
| 2022 | jobs at Skamania workplaces | 2,010 | 2,010 | 1,679 | 331 |

