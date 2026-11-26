# Heat and drought: synthesis

Date: 2026-11-12. Written by the research coordinator from the three reviewed findings files in this folder. Nothing here is a decision; decisions live in [architecture.md](../../architecture.md). What to do about it is in [RECOMMENDATIONS.md](../RECOMMENDATIONS.md).

| ID | File | Verdicts |
|---|---|---|
| H1 | [what-it-means.md](what-it-means.md) | 16 verified, 1 unsupported |
| H2 | [datasets.md](datasets.md) | 29 verified, 15 unsupported (all "not found" markers), 1 unreachable |
| H3 | [cheapest-honest-version.md](cheapest-honest-version.md) | 17 verified, 8 unsupported, 1 unreachable |

## How to read the evidence tags
- **[H2-13]** = claim 13 in file H2, marked `verified` by its reviewer. Only these carry a conclusion.
- **(R)** = something the reviewer found and opened while checking. Nobody checked the reviewer, so it is weaker than a verified claim.
- **not found** = searched for and not found, which is not proof of absence.
- **Limit of every verdict:** pages were read through a fetch tool that summarises and caps quotes at about 125 characters.
- **Hectare figures** are arithmetic on the stated grid size at about 45.7° N, not source claims.
- **No follow-up round was run.** Open gaps are listed at the end.

## Bottom line
1. **What we could honestly show is a hazard indicator or regional climate context, not a "risk".** Risk needs hazard, exposure and vulnerability [H1-7], and we have no exposure or vulnerability data for a plot (crop, irrigation, buildings).
2. **Nothing free was found that measures heat or drought at plot scale with a validated method.** The fine-resolution products are surface temperature under clear sky, or a vegetation index. The products that are well established are 9 km or coarser, so every plot in a cell gets the same number.
3. **One candidate is cheap and honest in scope:** a count of hot days per year from ERA5-Land, presented as regional context (about 9 km cells). It is a reanalysis, not an observation [H3-3], so it also sits at the edge of "based on past observations".
4. **It is still a new hazard,** which the constraints rate out of scope after the 22 Nov gate. It needs a new section in the evidence contract and an independent reference for validation. A Galați station series exists in GHCN-Daily (R), but its licence for our use is not established.
5. **Forecasts say nothing useful for a purchase,** and projections are regional scenario statements [H1-8, H1-9]. Both are roadmap material at most.
6. **Nothing verified is specific to Galați.** The drying trends found are for Sulina, Dobrogea and Romania as a whole [H1-15, H1-16, H1-17].

## 1. What "heat or drought risk for a plot" can honestly mean

### Definitions are local and statistical
- **Heatwave:** the WMO says heatwaves "are generally defined using local thresholds rather than a single global temperature value" [H1-1], and broadly as "a period of statistically unusual hot weather persisting for a number of days and nights" [H1-2].
- **Heat stress:** Copernicus counts days by "feels-like" category, with thresholds of 32, 38 and 46 °C for strong, very strong and extreme heat stress [H1-3].
- **Drought:** the EEA separates four types: meteorological (rainfall deficit), agricultural (soil moisture deficit), hydrological and socio-economic [H1-4, with the fourth type added by the reviewer]. Its indices are defined against a reference period: for example, a drought starts when the SPI falls below −1 for two consecutive months [H1-5].
- **Romania:** the national weather service's warnings page gives colour codes without numeric heat thresholds [H1-6]. That shows only that this page has none. A 35 °C rule and a 37 °C labour-law threshold are unopened leads.
- **So any count needs its own threshold, reference period and drought type, written down by us.** The ETCCDI definitions are a standard starting point: "summer days" as daily maximum above 25 °C, and a warm-spell index based on the 90th percentile (R).

### Hazard, exposure, vulnerability
- The IPCC defines risk as the potential for adverse consequences, and separates hazard, exposure and vulnerability [H1-7, read from a third-party mirror].
- With hazard data only, "risk" is the wrong word. The same hot summer means different things for an irrigated field, a dry field and a building plot.
- One exposure path that touches land buyers directly: clay shrinkage under drought can permanently damage buildings [H1-11, on a quote the reviewer supplied; France only]. Nothing was found for Romanian soils.

### Past observation, forecast, projection
| Kind | What it says | Use for a land buyer |
|---|---|---|
| Past observations or reanalysis | What was measured or reconstructed, with a stated threshold and period | The only kind that fits "a screening indicator based on past observations" |
| Seasonal forecast | "How likely it is that the coming season will be wetter, drier, warmer or colder than usual", with skill information needed [H1-8]. 1° grid [H2-44] | None for a purchase measured in decades (our inference from the timescale) |
| Climate projection | Scenario-conditional. The 0.11° EURO-CORDEX ensemble is "the best spatial resolution currently available from an ensemble of climate model projections for the whole of Europe" [H1-9, with the reviewer's fuller quote] | Roadmap only: "under scenario X the region shows change Y", never a plot prediction |

### How other products present it
- **ClimateCheck (vendor's own description):** projected hottest days around 2050, at about 5 km, with ratings "relative to the contiguous U.S. and Canada" [H1-12]. No independent validation of its heat score was found.
- **Independent critiques, by analogy only:** a CarbonPlan comparison found risk models "may agree over a region while diverging substantially at the property level" [H1-13]. It compared two firms on fire and flood, not heat. An industry benchmark of 13 vendors found "significant variation in both hazard and damage estimates" [H1-14].
- **Imoreview:** no heat or drought content was found (a search result only, not a verified claim).

### The pilot region
- South-eastern Romania: "a significant trend towards aridity especially from the 1980's" (a conference abstract centred on Sulina) [H1-15].
- Dobrogea: rising drought frequency 2001–2021 in a 1 km composite index [H1-16].
- Romania: "not immune to extreme weather events such as heatwaves, floods, soil droughts and storms" [H1-17].
- **None of these covers Galați County,** which is not in Dobrogea. A peer-reviewed 2022 paper by the same group reports significant August drying over the east and south-east (R, not filed as a claim). The H1 line "pilot hazard is real" is not backed and is not used here.

## 2. Datasets, sorted by what they are

### Reanalysis and gridded observations
| Dataset | Kind | Grid (about, in ha per cell) | Period | Licence | Tag |
|---|---|---|---|---|---|
| ERA5-Land | Reanalysis, "runs without data assimilation" | 9 km (8,000 ha) | 1950 to 2–3 months ago; a provisional stream about 5 days behind (R) | CC-BY | [H2-1, H2-2, H2-3, H2-4] |
| ERA5 | Reanalysis | 31 km (96,000 ha) | 1940 to present | CC-BY label on the data store | [H2-5] |
| CERRA | Regional reanalysis | 5.5 km (3,000 ha) | From Sept 1984; "to present" is not the real end of the data (R) | CC-BY | [H2-6] |
| E-OBS | Gridded station observations | Not stated on the page | 1950 to present | Two licences; the open one covers the EU. Licence text not read | [H2-7] |
| ROCADA | Romanian gridded observations | 0.1° | 1961–2013 | "Licensing unknown", on request | [H2-8] |
| UTCI (ERA5-HEAT) | Heat stress index from ERA5 | 0.25° (54,000 ha) | 1940 to near real time | Page still shows the old Copernicus licence name | [H2-11] |
| SPEIbase v2.11 | Drought index from station-based climate grids | 0.5° (about 200,000 ha) | 1901 to Dec 2024 | Open Database License, attribution | [H2-13] |

### Satellite surface temperature and vegetation
| Dataset | Grid | Period | Notes | Tag |
|---|---|---|---|---|
| MODIS MOD11A1 / MOD21A1D | 1 km (100 ha) | 2000 to present | "Openly shared, without restriction". Terra and Aqua begin shutting down in late 2026 or early 2027 (R) | [H2-16, H2-38] |
| VIIRS VNP21A1D (Suomi NPP) | 1 km | 2012 to 2 Nov 2026 | Delivery ceased on 2 November 2026. The NOAA-21 replacement starts 2023-02-10 (R) | [H2-37] |
| Landsat surface temperature | 30 m grid from a 100 m sensor | 1982 to present | 16-day repeat; known cloud error; "no restrictions on the use" | [H2-18, H2-19, H2-20, H3-9, H3-10] |
| ECOSTRESS | 70 m (0.5 ha) | 2018 to present | Irregular revisit, acquisition gaps | [H2-17] |
| HR-VPP Plant Phenology Index | 10 m | Oct 2016 to today | A vegetation index. "Full, open and free"; download needs authentication | [H2-35, H3-14] |
| NOAA VHI | 4 km | 1981 to present | "Provided for experimental use only" | [H2-22] |

- **No 1 km surface-temperature series is both long and continuing** (R): MODIS is ending, Suomi NPP has ended, and the replacement record starts in 2023.
- **Surface temperature is not air temperature.** In one peer-reviewed Landsat study (Miami, urban) the summer relationship between the two was "statistically insignificant" [H3-11]. A different climate and land cover, so it shows the kind of risk, not its size at Galați.
- **Landsat thermal detail is less than the grid suggests:** the 100 m data are resampled to 30 m (R), so a 1 ha plot holds about one independent sample. The overpass time also differs between Landsat missions (R).
- **A vegetation index is not a drought measurement.** Crop rotation, irrigation and bare soil all change it. No validated plot-level method was found.

### Ready-made indicators, projections, forecasts, soil
- **CDS "heat waves and cold spells":** 0.1°, labelled 1986–2085, CC-BY [H2-10, H3-5b]. It is model output only: 30-year smoothed averages from climate projections (R). Roadmap material, not history.
- **EURO-CORDEX on the CDS:** 0.11°, scenarios RCP 2.6, 4.5 and 8.5 to 2101, under a "CORDEX licence" that allows commercial use for the European domain [H2-42, H3-22, H3-23].
- **NEX-GDDP-CMIP6:** 0.25°, daily, CC0, no login [H2-25]. **CHELSA:** kilometre-scale downscaled products; licence not on the page [H2-26].
- **Seasonal forecasts:** 1° (about 860,000 ha), CC-BY plus an additional licence nobody opened [H2-44].
- **European Drought Observatory:** run by the JRC; data "can be freely downloaded" [H2-32]. The resolution, period and licence of its indicators were not found by anyone [H2-14]; the one factsheet was `unreachable`.
- **SoilGrids:** 250 m (6.25 ha), CC BY 4.0, per-pixel uncertainty; its REST API is paused [H2-40, H3-17]. Static soil context, not an observation of drought.

### Licence and access
- **Copernicus Climate Data Store:** the old "Licence to use Copernicus Products" was replaced by CC-BY on 2 July 2025 [H2-29]. CC BY 4.0 allows use "for any purpose, even commercially", with credit and an indication of changes [H2-30]. The exact attribution string is not fixed; each dataset's "References" section gives it.
- **Access to the data store (R):** an account, a personal token, and accepting each dataset's terms by hand once. Scriptable after that. The token is a secret and stays out of git.
- **NASA Earthdata:** "login needed but scriptable" has no verified claim behind it.
- **Usable in a product on the licence text read so far:** ERA5-Land, CERRA, SPEIbase (attribution; share-alike consequences unread), NEX-GDDP, MODIS, Landsat, HR-VPP, SoilGrids. **Not established:** E-OBS, the drought observatory, CHELSA, the seasonal forecasts' extra licence.

## 3. The cheapest honest version (H3)
| Candidate | What it would be | Why it is or isn't cheap and honest |
|---|---|---|
| **(a) ERA5-Land hot-day count** | Days per year with daily maximum 2 m temperature above one written threshold, per 9 km cell | The only cheap one. Region-level only. Conditions below |
| (b) Landsat surface-temperature climatology | Mean clear-sky summer surface temperature per pixel | Heavy (many scenes, cloud masks, mixed overpass times). Surface temperature, not air temperature. No field-scale reference found |
| (c) Vegetation-stress history (HR-VPP) | Anomalies of a vegetation index | Heavy. Confounded by rotation, irrigation and bare soil. No validation design found |
| (d) Soil water-holding context (SoilGrids) | A static soil property | Not a hazard observation. Access to the water-retention product not established |

**Candidate (a), in verified facts**
- **Data:** the data store's "ERA5-Land daily statistics" gives daily maximum, mean or minimum 2 m temperature, 0.1° (native 9 km), January 1950 to present, CC-BY, as NetCDF. The daily value is computed at retrieval [H3-1, H3-2, H3-5].
- **What it is:** "a replay of the land component of the ERA5 climate reanalysis"; observations influence it only indirectly [H3-3]. It must be labelled a reanalysis, not a measurement.
- **Scale:** one cell is about 8,000 ha [H3-4], so it describes the region and every plot in a cell gets the same value.
- **Tooling:** `cdsapi` is a pure-Python wheel [H3-6]. `netCDF4` has stable-ABI wheels for Linux and macOS that should install on 3.14, and `h5py`, `pandas` and `pyproj` have 3.14 wheels (R; nothing was install-tested). The H3 statement that Linux has no usable `netCDF4` wheel was `unsupported`.
- **Known weakness, unverified:** search results suggest ERA5-Land underestimates extreme daily maxima in some settings (R, not opened). A hot-day count above a fixed threshold is sensitive to exactly that.

**What validation could look like**
- **A station exists (R).** GHCN-Daily lists `ROE00108895` "GALATI, RO" with daily maximum temperature from 1953 to November 2026. This contradicts claim H3-21 ("not found"). It was read through a tool summary; confirm by hand.
- **Its licence is open.** The "E" in the ID marks an identifier from the ECA&D station dataset (R). ECA&D says part of its data is free "for non-commercial research and education" [H3-19]. Nobody could read the policy itself. GHCN-Daily's product page states no licence and warns the data are not homogenized [H3-20].
- **It would be a thin test.** One station against one 9 km cell allows a split by years only, and ERA5-Land is not fully independent of station observations [H3-3].
- **E-OBS** is the observation-based alternative that was not weighed (R). It is built from the same station network, so it could replace ERA5-Land as the layer but not serve as an independent reference for the Galați station.

**Not used from H3:** the effort figures (15–25, 40–70, 50–80 person-hours) are the researcher's own estimates; "ECA&D terms exclude product use" goes beyond what was read; "scriptable: yes" and "fits 3.14: likely" in its table have no backing claim.

## What could not be used
- **H1:** claim 10 (plot-scale surface temperature; no quote). The four wording options in its relevance section are the researcher's own synthesis, not sourced rules.
- **H2:** the 15 "not found" markers (9, 12, 15, 21, 23, 24, 27, 28, 31, 34, 36, 39, 41, 43, 45) and claim 33 (`unreachable`: drought-indicator factsheet). The area figure in claim 44 is wrong (about 860,000 ha, not 600,000).
- **H3:** claims 7 (`netCDF4` conclusion), 8, 13, 15, 18, 24, 25 (no source), 21 (contradicted), 16 (`unreachable`: Romanian MODIS drought study).

## Where sources disagree
- **Is there an open station series for Galați?** The H3 researcher found none; the reviewer found a current GHCN-Daily series whose licence is unclear.
- **`netCDF4` on Python 3.14:** the researcher read "no standard Linux wheel"; the reviewer found stable-ABI wheels on the same page.
- **Data store licence labels:** CC-BY since 2 July 2025, yet the UTCI page still showed the old licence name on 12 Nov 2026 [H2-29, H2-11].
- **Landsat on the Planetary Computer:** the collection's licence field says "proprietary" while its licence link says "Public Domain" [H3-9]; USGS says "no restrictions" [H2-20].
- **CERRA and the heat-spell dataset:** both pages read as current or historical, while forum posts and the dataset description show a lagging end date and model-only content (R).

## Open after this round (no follow-up was run)
- The licence of the GHCN-Daily Galați series and the ECA&D data policy text; whether a validation-only reference needs a product licence at all (the lead's call).
- The E-OBS open data licence text and grid spacing.
- European Drought Observatory indicators: resolution, period and licence.
- ERA5-Land bias for hot extremes.
- An official Romanian heatwave definition.
- Any peer-reviewed trend for Galați or the Bărăgan specifically.
