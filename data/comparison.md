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

Values compared: 90 (30 home-work pairs x 3 years). Exact matches: 90. Mismatches: 0.

- same-state: 36 values, 36 match, 0 do not
- cross-state: 54 values, 54 match, 0 do not

By the label the page's code comment gives the cell:

| Page label | Pairs | Values | Match | Do not match |
|---|--:|--:|--:|--:|
| CONFIRMED | 0 | 0 | 0 | 0 |
| from summary | 0 | 0 | 0 | 0 |
| estimate | 0 | 0 | 0 | 0 |
| no label | 30 | 90 | 90 | 0 |
| zero, 'below threshold' | 0 | 0 | 0 | 0 |

## Same-state pairs (LODES main files)

| Home → Work | Page label | 2012 page | 2012 LODES | 2019 page | 2019 LODES | 2022 page | 2022 LODES | Years matching |
|---|---|--:|--:|--:|--:|--:|--:|---|
| Wasco → Hood River | no label | 1,080 | 1,080 | 1,422 | 1,422 | 1,430 | 1,430 | 2012, 2019, 2022 |
| Wasco → Multnomah | no label | 1,109 | 1,109 | 966 | 966 | 1,037 | 1,037 | 2012, 2019, 2022 |
| Hood River → Wasco | no label | 737 | 737 | 734 | 734 | 758 | 758 | 2012, 2019, 2022 |
| Hood River → Multnomah | no label | 764 | 764 | 768 | 768 | 929 | 929 | 2012, 2019, 2022 |
| Klickitat → Skamania | no label | 352 | 352 | 97 | 97 | 101 | 101 | 2012, 2019, 2022 |
| Klickitat → Clark | no label | 694 | 694 | 232 | 232 | 365 | 365 | 2012, 2019, 2022 |
| Skamania → Klickitat | no label | 424 | 424 | 386 | 386 | 332 | 332 | 2012, 2019, 2022 |
| Skamania → Clark | no label | 1,030 | 1,030 | 954 | 954 | 1,068 | 1,068 | 2012, 2019, 2022 |
| Clark → Klickitat | no label | 294 | 294 | 426 | 426 | 397 | 397 | 2012, 2019, 2022 |
| Clark → Skamania | no label | 273 | 273 | 298 | 298 | 328 | 328 | 2012, 2019, 2022 |
| Multnomah → Hood River | no label | 380 | 380 | 758 | 758 | 645 | 645 | 2012, 2019, 2022 |
| Multnomah → Wasco | no label | 282 | 282 | 285 | 285 | 349 | 349 | 2012, 2019, 2022 |

## Cross-state pairs (LODES aux files)

| Home → Work | Page label | 2012 page | 2012 LODES | 2019 page | 2019 LODES | 2022 page | 2022 LODES | Years matching |
|---|---|--:|--:|--:|--:|--:|--:|---|
| Wasco → Klickitat | no label | 294 | 294 | 429 | 429 | 413 | 413 | 2012, 2019, 2022 |
| Wasco → Skamania | no label | 23 | 23 | 10 | 10 | 36 | 36 | 2012, 2019, 2022 |
| Wasco → Clark | no label | 64 | 64 | 69 | 69 | 80 | 80 | 2012, 2019, 2022 |
| Hood River → Klickitat | no label | 388 | 388 | 570 | 570 | 428 | 428 | 2012, 2019, 2022 |
| Hood River → Skamania | no label | 73 | 73 | 83 | 83 | 81 | 81 | 2012, 2019, 2022 |
| Hood River → Clark | no label | 55 | 55 | 56 | 56 | 73 | 73 | 2012, 2019, 2022 |
| Klickitat → Hood River | no label | 719 | 719 | 769 | 769 | 753 | 753 | 2012, 2019, 2022 |
| Klickitat → Wasco | no label | 478 | 478 | 553 | 553 | 507 | 507 | 2012, 2019, 2022 |
| Klickitat → Multnomah | no label | 514 | 514 | 406 | 406 | 588 | 588 | 2012, 2019, 2022 |
| Skamania → Hood River | no label | 321 | 321 | 383 | 383 | 343 | 343 | 2012, 2019, 2022 |
| Skamania → Wasco | no label | 86 | 86 | 60 | 60 | 60 | 60 | 2012, 2019, 2022 |
| Skamania → Multnomah | no label | 681 | 681 | 662 | 662 | 660 | 660 | 2012, 2019, 2022 |
| Clark → Hood River | no label | 170 | 170 | 229 | 229 | 245 | 245 | 2012, 2019, 2022 |
| Clark → Wasco | no label | 123 | 123 | 110 | 110 | 107 | 107 | 2012, 2019, 2022 |
| Clark → Multnomah | no label | 44,052 | 44,052 | 49,818 | 49,818 | 44,936 | 44,936 | 2012, 2019, 2022 |
| Multnomah → Klickitat | no label | 103 | 103 | 90 | 90 | 115 | 115 | 2012, 2019, 2022 |
| Multnomah → Skamania | no label | 55 | 55 | 64 | 64 | 88 | 88 | 2012, 2019, 2022 |
| Multnomah → Clark | no label | 8,814 | 8,814 | 11,407 | 11,407 | 10,946 | 10,946 | 2012, 2019, 2022 |

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
| 2012 | jobs held by Skamania residents | 5,410 | 5,410 | 3,626 | 1,784 |
| 2012 | of those, at Skamania workplaces | 1,101 | 1,101 | | |
| 2012 | of those, outside Skamania | 4,309 | 4,309 | | |
| 2012 | share outside Skamania | 79.6% | 79.6% | | |
| 2012 | jobs at Skamania workplaces | 2,264 | 2,264 | 1,974 | 290 |
| 2019 | jobs held by Skamania residents | 5,618 | 5,618 | 3,709 | 1,909 |
| 2019 | of those, at Skamania workplaces | 1,253 | 1,253 | | |
| 2019 | of those, outside Skamania | 4,365 | 4,365 | | |
| 2019 | share outside Skamania | 77.7% | 77.7% | | |
| 2019 | jobs at Skamania workplaces | 2,210 | 2,210 | 1,901 | 309 |
| 2022 | jobs held by Skamania residents | 5,698 | 5,698 | 3,821 | 1,877 |
| 2022 | of those, at Skamania workplaces | 1,106 | 1,106 | | |
| 2022 | of those, outside Skamania | 4,592 | 4,592 | | |
| 2022 | share outside Skamania | 80.6% | 80.6% | | |
| 2022 | jobs at Skamania workplaces | 2,010 | 2,010 | 1,679 | 331 |

