// ── Flow data from raw LODES8 origin-destination files ───────────────────────
// FLOWS[home_fips][work_fips] = {2012, 2019, 2022}, in jobs (S000, job type JT00).
// Every value is computed by scripts/recompute_flows.py from the Census Bureau's
// main AND aux files for Oregon and Washington. Same-state pairs come from main.
// Cross-state pairs come from aux. County = first five digits of the block geocode.
const FLOWS = {
  "41065": { // Wasco home
    "41027": { 2012:  1080, 2019:  1422, 2022:  1430 }, // → Hood River (main)
    "53059": { 2012:    23, 2019:    10, 2022:    36 }, // → Skamania (aux)
    "53039": { 2012:   294, 2019:   429, 2022:   413 }, // → Klickitat (aux)
    "53011": { 2012:    64, 2019:    69, 2022:    80 }, // → Clark (aux)
    "41051": { 2012:  1109, 2019:   966, 2022:  1037 }, // → Multnomah (main)
  },
  "41027": { // Hood River home
    "41065": { 2012:   737, 2019:   734, 2022:   758 }, // → Wasco (main)
    "53059": { 2012:    73, 2019:    83, 2022:    81 }, // → Skamania (aux)
    "53039": { 2012:   388, 2019:   570, 2022:   428 }, // → Klickitat (aux)
    "53011": { 2012:    55, 2019:    56, 2022:    73 }, // → Clark (aux)
    "41051": { 2012:   764, 2019:   768, 2022:   929 }, // → Multnomah (main)
  },
  "53039": { // Klickitat home
    "41027": { 2012:   719, 2019:   769, 2022:   753 }, // → Hood River (aux)
    "41065": { 2012:   478, 2019:   553, 2022:   507 }, // → Wasco (aux)
    "53059": { 2012:   352, 2019:    97, 2022:   101 }, // → Skamania (main)
    "53011": { 2012:   694, 2019:   232, 2022:   365 }, // → Clark (main)
    "41051": { 2012:   514, 2019:   406, 2022:   588 }, // → Multnomah (aux)
  },
  "53059": { // Skamania home
    "41027": { 2012:   321, 2019:   383, 2022:   343 }, // → Hood River (aux)
    "41065": { 2012:    86, 2019:    60, 2022:    60 }, // → Wasco (aux)
    "53039": { 2012:   424, 2019:   386, 2022:   332 }, // → Klickitat (main)
    "53011": { 2012:  1030, 2019:   954, 2022:  1068 }, // → Clark (main)
    "41051": { 2012:   681, 2019:   662, 2022:   660 }, // → Multnomah (aux)
  },
  "53011": { // Clark home
    "41027": { 2012:   170, 2019:   229, 2022:   245 }, // → Hood River (aux)
    "41065": { 2012:   123, 2019:   110, 2022:   107 }, // → Wasco (aux)
    "53039": { 2012:   294, 2019:   426, 2022:   397 }, // → Klickitat (main)
    "53059": { 2012:   273, 2019:   298, 2022:   328 }, // → Skamania (main)
    "41051": { 2012: 44052, 2019: 49818, 2022: 44936 }, // → Multnomah (aux)
  },
  "41051": { // Multnomah home
    "41027": { 2012:   380, 2019:   758, 2022:   645 }, // → Hood River (main)
    "41065": { 2012:   282, 2019:   285, 2022:   349 }, // → Wasco (main)
    "53039": { 2012:   103, 2019:    90, 2022:   115 }, // → Klickitat (aux)
    "53059": { 2012:    55, 2019:    64, 2022:    88 }, // → Skamania (aux)
    "53011": { 2012:  8814, 2019: 11407, 2022: 10946 }, // → Clark (aux)
  },
};

// ── Skamania residence and workplace totals (same script) ────────────────────
// total = jobs at Oregon and Washington workplaces held by Skamania residents.
const SKAMANIA_FISCAL = {
  2012: { total: 5410, local: 1101, out: 4309, pctOut: 79.6, totalJobs: 2264 },
  2019: { total: 5618, local: 1253, out: 4365, pctOut: 77.7, totalJobs: 2210 },
  2022: { total: 5698, local: 1106, out: 4592, pctOut: 80.6, totalJobs: 2010 },
};
