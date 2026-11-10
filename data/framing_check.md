# Framing check

Source: U.S. Census Bureau, LEHD, LODES version 8, origin-destination files (main + aux, Oregon and
Washington), job type JT00, column S000. Data years 2012, 2019, 2022. All figures are jobs.
Made by `scripts/framing_check.py`.

## 1. Jobs at workplaces in each county

| County | 2012 | 2019 | 2022 | 2012 to 2019 | 2019 to 2022 | 2012 to 2022 | Jobs added or lost, 2012 to 2022 |
|---|--:|--:|--:|--:|--:|--:|--:|
| Hood River | 11,203 | 13,625 | 13,335 | +21.6% | -2.1% | +19.0% | +2,132 |
| Wasco | 9,243 | 10,027 | 9,924 | +8.5% | -1.0% | +7.4% | +681 |
| Klickitat | 6,364 | 7,127 | 6,972 | +12.0% | -2.2% | +9.6% | +608 |
| Skamania | 2,264 | 2,210 | 2,010 | -2.4% | -9.0% | -11.2% | -254 |
| Four Gorge counties | 29,074 | 32,989 | 32,241 | +13.5% | -2.3% | +10.9% | +3,167 |

## 2. Every flow between two of the four Gorge counties, largest first (2022)

| Home → Work | Crosses the river | 2012 | 2019 | 2022 | Change in jobs, 2012 to 2022 | Percent |
|---|---|--:|--:|--:|--:|--:|
| Wasco → Hood River | no | 1,080 | 1,422 | 1,430 | +350 | +32.4% |
| Hood River → Wasco | no | 737 | 734 | 758 | +21 | +2.8% |
| Klickitat → Hood River | yes | 719 | 769 | 753 | +34 | +4.7% |
| Klickitat → Wasco | yes | 478 | 553 | 507 | +29 | +6.1% |
| Hood River → Klickitat | yes | 388 | 570 | 428 | +40 | +10.3% |
| Wasco → Klickitat | yes | 294 | 429 | 413 | +119 | +40.5% |
| Skamania → Hood River | yes | 321 | 383 | 343 | +22 | +6.9% |
| Skamania → Klickitat | no | 424 | 386 | 332 | -92 | -21.7% |
| Klickitat → Skamania | no | 352 | 97 | 101 | -251 | -71.3% |
| Hood River → Skamania | yes | 73 | 83 | 81 | +8 | +11.0% |
| Skamania → Wasco | yes | 86 | 60 | 60 | -26 | -30.2% |
| Wasco → Skamania | yes | 23 | 10 | 36 | +13 | +56.5% |

## 3. Net flow for each pair of Gorge counties

Net = jobs held in the second county by residents of the first, minus the reverse.

| Pair | Crosses the river | 2012 net | 2019 net | 2022 net |
|---|---|--:|--:|--:|
| Wasco → Hood River minus reverse | no | +343 | +688 | +672 |
| Klickitat → Hood River minus reverse | yes | +331 | +199 | +325 |
| Klickitat → Wasco minus reverse | yes | +184 | +124 | +94 |
| Skamania → Hood River minus reverse | yes | +248 | +300 | +262 |
| Skamania → Klickitat minus reverse | no | +72 | +289 | +231 |
| Skamania → Wasco minus reverse | yes | +63 | +50 | +24 |

## 4. Who holds the jobs at Hood River County workplaces

| Home of job holder | 2012 jobs | 2012 share | 2019 jobs | 2019 share | 2022 jobs | 2022 share | Change in jobs, 2012 to 2022 |
|---|--:|--:|--:|--:|--:|--:|--:|
| Hood River | 6,134 | 54.8% | 7,654 | 56.2% | 7,354 | 55.1% | +1,220 |
| Wasco | 1,080 | 9.6% | 1,422 | 10.4% | 1,430 | 10.7% | +350 |
| Klickitat | 719 | 6.4% | 769 | 5.6% | 753 | 5.6% | +34 |
| Skamania | 321 | 2.9% | 383 | 2.8% | 343 | 2.6% | +22 |
| Klickitat + Skamania together | 1,040 | 9.3% | 1,152 | 8.5% | 1,096 | 8.2% | +56 |
| Multnomah | 380 | 3.4% | 758 | 5.6% | 645 | 4.8% | +265 |
| Clark | 170 | 1.5% | 229 | 1.7% | 245 | 1.8% | +75 |
| Everywhere else | 2,399 | 21.4% | 2,410 | 17.7% | 2,565 | 19.2% | +166 |
| All jobs at Hood River workplaces | 11,203 | 100.0% | 13,625 | 100.0% | 13,335 | 100.0% | +2,132 |

## 5. Jobs held by each Gorge county's residents (Oregon and Washington workplaces)

A job in a third state would be in that state's aux file, which was not read.

| Home county | Year | Jobs held by residents | In home county | Outside home county | Share outside | In the other state |
|---|---|--:|--:|--:|--:|--:|
| Hood River | 2012 | 10,410 | 6,134 | 4,276 | 41.1% | 846 |
| Hood River | 2019 | 11,865 | 7,654 | 4,211 | 35.5% | 971 |
| Hood River | 2022 | 12,023 | 7,354 | 4,669 | 38.8% | 932 |
| Wasco | 2012 | 11,468 | 5,269 | 6,199 | 54.1% | 825 |
| Wasco | 2019 | 12,131 | 6,003 | 6,128 | 50.5% | 1,006 |
| Wasco | 2022 | 11,878 | 5,627 | 6,251 | 52.6% | 965 |
| Klickitat | 2012 | 8,156 | 3,194 | 4,962 | 60.8% | 2,392 |
| Klickitat | 2019 | 7,681 | 3,420 | 4,261 | 55.5% | 2,479 |
| Klickitat | 2022 | 8,642 | 3,454 | 5,188 | 60.0% | 2,885 |
| Skamania | 2012 | 5,410 | 1,101 | 4,309 | 79.6% | 1,784 |
| Skamania | 2019 | 5,618 | 1,253 | 4,365 | 77.7% | 1,909 |
| Skamania | 2022 | 5,698 | 1,106 | 4,592 | 80.6% | 1,877 |

