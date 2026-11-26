# What is the cheapest honest version of a heat or drought layer that fits our architecture, what would it take, and what belongs on the roadmap? (H3)
Date: 2026-11-12
Scope: two to four candidate layers, each one dataset plus one simple indicator precomputed into a COG for Galati; access, licence, wheels, claims and limits, validation feasibility, effort basis, roadmap items. Out of bounds: the full dataset inventory, definitions of heatwave/drought, flood, ground motion, ML. The two earlier files (`what-it-means.md`, `datasets.md`) were used only as a map; every claim below was opened by me. Tool output was a summary of each page, so only text the tool returned inside quotation marks is used as a quote; those claims are capped at medium confidence unless the source is a primary catalogue page. Hours and cell counts are my own estimates or arithmetic, marked as such. No page tried to instruct me.

## Claims

### A. Candidate (a): hot-day count from ERA5-Land daily statistics (regional context)
1. **Claim:** ERA5-Land daily statistics on the CDS give daily max/mean/min of 2 m temperature at 0.1 deg (native 9 km), 1950 to present, CC-BY, NetCDF in a zip. The daily value is computed at retrieval, not archived.
   - Source: https://cds.climate.copernicus.eu/datasets/derived-era5-land-daily-statistics?tab=overview
   - Quote: "January 1950 to present"; "0.1° x 0.1°; Native resolution is 9 km."; "NetCDF (in zip archive)"; "the daily aggregation is calculated during the retrieval process and is not part of a permanently archived dataset."
   - Source date: 2026 (page current at fetch)
   - Source type: official docs
   - Confidence: medium (tool summary, quotes in quotation marks)
2. **Claim:** The same page offers the aggregation as a choice (mean, max, min), so a daily maximum of 2 m temperature is obtainable.
   - Source: https://cds.climate.copernicus.eu/datasets/derived-era5-land-daily-statistics?tab=overview
   - Quote: "The daily aggregation statistic (daily mean, daily max, daily min)."
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
3. **Claim:** ERA5-Land is not independent of observations: it is forced by ERA5, which is influenced by observations, and it is a replay of the land component.
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
   - Quote: "ERA5-Land is a replay of the land component of the ERA5 climate reanalysis, forced by meteorological fields from ERA5."; "Observations indirectly influence the simulation through the atmospheric forcing of ERA5."
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
4. **Claim:** A plot inherits its 9 km cell. Resolution is 9 km; my arithmetic: about 8,000 ha per cell, so a Galati County extract (roughly 100 cells, my estimate) x 30 years of daily values is a few hundred thousand numbers, small.
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
   - Quote: "The ERA5-Land HRES dataset has been produced at a resolution of 9 km, (~0.08°)"
   - Source date: 2026
   - Source type: official docs
   - Confidence: high for resolution; extract size is my estimate, not a source
5. **Claim:** The CDS dataset pages show a CC-BY licence; CC BY 4.0 permits commercial use and adaptation with attribution.
   - Source: https://cds.climate.copernicus.eu/datasets/derived-era5-land-daily-statistics?tab=overview ; https://creativecommons.org/licenses/by/4.0/
   - Quote: "CC-BY licence" (CDS page); "copy and redistribute the material in any medium or format for any purpose, even commercially." (CC page)
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium (CDS licence label; the CC text is the licence itself)
5b. **Claim:** The CDS "heat and cold spells in Europe" dataset is NOT a past-observation product: its statistics are 30-year smoothed averages from 1971 to 2100 under climate scenarios, 1986 to 2085, 0.1 deg, "No updates expected". It therefore belongs with projections (roadmap), not candidate (a).
   - Source: https://cds.climate.copernicus.eu/datasets/sis-heat-and-cold-spells?tab=overview
   - Quote: "From 1986 to 2085"; "CC-BY licence"; "No updates expected" (tool summary; the 1971-2100 smoothing and scenario wording was paraphrased by the tool, not quoted)
   - Source date: 2019-11-07 published, 2026-05-12 updated (as shown on page)
   - Source type: official docs
   - Confidence: medium
6. **Claim:** The CDS API client `cdsapi` is a pure-Python wheel installable on 3.14; account and key are still required (manual one-time account creation, then scriptable).
   - Source: https://pypi.org/project/cdsapi/#files
   - Quote: "cdsapi-0.7.7-py2.py3-none-any.whl" (version 0.7.7, 2025-09-30, Requires Python >=3.8, as returned by the page summary)
   - Source date: 2025-09-30
   - Source type: official docs (PyPI)
   - Confidence: medium (the need for a CDS account is not quoted from a source here: not found)
7. **Claim:** Python 3.14 wheels. xarray 2026.9.0 and rioxarray 0.24.0 (lists a 3.14 classifier) and odc-stac 0.5.3 are pure-Python wheels. netCDF4 1.7.5.1.post1 has standard cp314 wheels only for Windows (amd64, arm64); for Linux and macOS the listing shows only free-threaded cp314t wheels, so a standard Linux 3.14 install may need a source build or another NetCDF reader. h5netcdf: not found (page failed to load). pystac-client, rasterio, numpy and scipy are already resolved in the repo's `uv.lock` for `requires-python >=3.14`. Whether rasterio's GDAL can read the CDS NetCDF/GRIB: not found.
   - Source: https://pypi.org/project/netCDF4/#files ; https://pypi.org/project/rioxarray/#files ; https://pypi.org/project/xarray/#files ; https://pypi.org/project/odc-stac/#files
   - Quote: "netcdf4-1.7.5.1.post1-cp314-cp314-win_amd64.whl"; "netcdf4-1.7.5.1.post1-cp314-cp314t-manylinux_2_28_x86_64.whl"; "rioxarray-0.24.0-py3-none-any.whl"; "xarray-2026.9.0-py3-none-any.whl"; "odc_stac-0.5.3-py3-none-any.whl"
   - Source date: 2026-07 to 2026-10 (release dates on the pages)
   - Source type: official docs (PyPI)
   - Confidence: medium (page summaries; the "only" claim for Linux rests on the listing the tool returned)
8. **Claim:** Hot-day definition (one per indicator). ETCCDI "summer days" or similar threshold count: not fetched, not found. Whichever definition the team picks must be written before any test.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

### B. Candidate (b): Landsat surface-temperature climatology
9. **Claim:** Landsat Collection 2 Level-2 surface temperature is on the Planetary Computer STAC API (collection `landsat-c2-l2`, 1982 to present, ST_B10 band, scale 0.00341802 K with offset 149). The collection licence field reads "proprietary" while a linked entry is "Public Domain"; the page does not reconcile them and says nothing on login.
   - Source: https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2
   - Quote: "Collection 2 Level-2 Science Products are available from August 22, 1982 to present."; "Collection 2 Level-2 Thermal Infrared Band (ST_B10) Surface Temperature."
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
10. **Claim:** USGS states the product carries a known cloud error and measures surface (not air) temperature.
    - Source: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
    - Quote: "A known error exists in the surface temperature retrievals relative to clouds and possibly cloud shadows."; "Landsat surface temperature measures the Earth's surface temperature in Kelvin."
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
11. **Claim:** In a peer-reviewed Landsat 8 study (Miami-Dade, subtropical, urban, 30 m, about 11 AM overpass, 98 of 260 scenes kept after cloud and quality filtering, 7 stations) the summer LST-air temperature relationship was not significant. This is a different climate and land cover from Galati cropland, so it shows the kind of risk, not its size here.
    - Source: https://journals.plos.org/climate/article?id=10.1371/journal.pclm.0000278
    - Quote: "The relationship between LST and SAT during the summer is statistically insignificant."; "LST remains a proxy for the spatial patterns of SAT," but "its accuracy in capturing the magnitude of SAT is limited annually."
    - Source date: 2024-10
    - Source type: peer-reviewed
    - Confidence: medium (via tool summary; limited transfer to Galati)
12. **Claim:** The thermal band is sensed at 100 m and the overpass is fixed at about 10:12 local solar time (so a Landsat LST says nothing about afternoon maxima).
    - Source: https://www.usgs.gov/landsat-missions/landsat-9
    - Quote: "TIRS provides two spectral bands with a maximum ground sampling distance, both in-track and cross track, of 100 m (328 ft) for both bands."; "Has a 16-day repeat cycle with an equatorial crossing time of 10:12 a.m. +/- 5 minutes"
    - Source date: 2026 (quotes carried from the unreviewed datasets file; I did not reopen this page: recheck before use)
    - Source type: official docs
    - Confidence: low (not reopened by me)
13. **Claim:** Published field-scale validation of thermal-based crop stress against independent reference exists only partly: for ECOSTRESS (70 m) the search found DisALEXI-JPL evapotranspiration compared with in situ ET and ECOSTRESS LST validated at radiation-network stations (not croplands). A parcel-level validation of an LST-based heat indicator on cropland: not found.
    - Source: not found (search results only; full texts not opened)
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### C. Candidate (c): vegetation-stress history (HR-VPP PPI or Sentinel-2)
14. **Claim:** CLMS HR-VPP Plant Phenology Index is 10 m on the Sentinel-2 tiling grid, October 2016 to today. Download from CLMS or WEkEO is marked as requiring authentication; OpenSearch/WMS/WMTS links carry no such note. Licence: "full, open and free access" with attribution and no-endorsement conditions. Each file has a QFLAG2 quality indicator for clouds, shadows, snow, water. No formal accuracy assessment is described on the record.
    - Source: https://sdi.eea.europa.eu/catalogue/copernicus/api/records/65f095af-5225-490b-8a29-4500d4c31b8a
    - Quote: "for the period from October 2016 until today, with daily updates"; "The Copernicus land monitoring products and services are made available on a principle of full, open and free access"; "Download (requires authentication)" (tool summary of the link labels)
    - Source date: 2021-09 (product version); fetched 2026
    - Source type: official docs
    - Confidence: medium
15. **Claim:** HR-VPP download goes through a WEkEO or EU Login token (a one-time manual account step) and acceptance of the CLMS data policy; this counts against "scripted without a manual login". Source is a search-result summary, official CLMS API docs not opened.
    - Source: not found (not opened)
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low
16. **Claim:** Romanian drought studies using MODIS or Sentinel-2 indices validated against meteorological data, soil moisture and agricultural production (2001-2019 MODIS Drought Severity Index in three plains) exist, but I could not open the full text (HTTP 403 / binary PDF); how the validation was split: not found. Confounders (crop rotation, irrigation, bare soil) as published statements: not found.
    - Source: https://www.mdpi.com/2072-4292/12/23/3940 (not opened: 403)
    - Quote: not found
    - Source date: 2020
    - Source type: peer-reviewed (existence only, from search results)
    - Confidence: low

### D. Candidate (d): soil water-holding capacity context
17. **Claim:** SoilGrids is 250 m, six depth intervals, CC-BY 4.0, per-pixel uncertainty quantified; the REST API is paused and the page points to other access routes. Water retention is a separate WoSIS-based product (title "Global mapping of volumetric water retention at 100, 330 and 15 000 cm suction using the WoSIS database"); whether it is downloadable and any local-scale warning: not found. A 250 m cell is 6.25 ha (my arithmetic).
    - Source: https://www.isric.org/explore/soilgrids ; https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs.html
    - Quote: "at a spatial resolution of 250 meters"; "CC-BY 4.0 License"; "The uncertainty of the predictions is quantified for each pixel."
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
18. **Claim:** Soil data say nothing about past events; a soil layer is a static context, not an observation of heat or drought. (My reading; no source needed beyond claim 17.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### E. Validation references
19. **Claim:** ECA&D station data are free only "for non-commercial research and education"; the full policy page was not reachable (404), so product use is not covered by what I verified.
    - Source: https://www.ecad.eu/dailydata/index.php
    - Quote: "Part of the dataset is freely available for non-commercial research and education."
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
20. **Claim:** NOAA GHCN-Daily has daily max/min temperature and precipitation as per-station text files over HTTPS (no login stated), but the product page states no licence, and warns the data are not homogenised.
    - Source: https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
    - Quote: "Because GHCNd has not been homogenized to account for artifacts" (tool summary; the access sentence "individual ASCII (i.e., plain text) files" also returned in quotes)
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
21. **Claim:** A current Galati or nearby station in GHCN-Daily, ISD, or from the Romanian meteorological service (ANM) with open licence: NOT FOUND. The only hit was a Berkeley Earth listing of a "GALATI" series ending 2013 (secondary, stale). The GHCN country code for Romania is RO ("RO Romania").
    - Source: https://berkeleyearth.org/temperature-station-list/prefix/GALAT ; https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-countries.txt
    - Quote: "RO Romania"
    - Source date: 2026
    - Source type: official docs (country list); blog/secondary (Berkeley listing, not opened by me)
    - Confidence: low

### F. Roadmap material
22. **Claim:** EURO-CORDEX Europe domain is 0.11 deg, RCP 2.6/4.5/8.5, to 2101, and the CDS page says commercial use is allowed with exceptions for two RCMs.
    - Source: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview
    - Quote: "European domain: 0.11°x0.11°"; "These scenarios are the RCP 2.6, 4.5 and 8.5 scenarios."; "The data can be used for commercial purposes (unrestricted use)"
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
23. **Claim:** The EURO-CORDEX reference paper describes 12.5 km ensemble simulations for two emission scenarios and compares them with earlier ENSEMBLES simulations (Jacob et al., Regional Environmental Change 14, 2014). Wording for the product: scenario projections, not predictions for a plot (my wording rule, not a source claim).
    - Source: https://research.vu.nl/en/publications/euro-cordex-new-high-resolution-climate-change-projections-for-eu/
    - Quote: "A new high-resolution regional climate change ensemble has been established for Europe"
    - Source date: 2014
    - Source type: peer-reviewed
    - Confidence: medium
24. **Claim:** A field-scale operational use of thermal data exists: a NASA slide deck says Land IQ uses ECOSTRESS surface temperature as one input to field-by-field ET (California). Presentation only, not opened by me.
    - Source: not found (search result only)
    - Quote: not found
    - Source date: 2026-02
    - Source type: vendor
    - Confidence: low
25. **Claim:** Irrigation access, groundwater and exposure/vulnerability data for Galati: not found.
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

## Relevance to LandHorizon
**Evidence contract.** Any heat or drought layer adds a new section to the evidence JSON (Pydantic models in `api/main.py`). That changes the contract the frontend depends on and needs the team lead's review before any code, ideally at or before the 22 Nov gate.

**Per candidate**
- **(a) ERA5-Land hot-day count per year (regional context).** Pipeline: `cdsapi` request for daily max 2 m temperature over a Galati box, count days above one written threshold per year, write a ~9 km COG; API reads the cell. Licence CC-BY (attribution string: not found). Access needs a CDS account/key (manual once), no Earth Engine. Python: cdsapi, xarray, rioxarray fine; netCDF4 has no standard Linux cp314 wheel (claim 7), so reading may need a source build or Windows-only runs. Extract is tiny (claim 4). Coverage: whole of Galati; every plot in a cell gets the same number, so it must be presented as describing the region (about 8,000 ha), and plots straddling cells get one or more cells. It is reanalysis, not an observation. `unknown` case: plot outside the extract, masked/missing cell, or request failure; never zero. Effort (my estimate, not a source): about 15-25 person-hours for one person (account, request, threshold, COG, contract section, text). Validation: ERA5-Land is forced by ERA5, which observations influence (claim 3), so a station is only partly independent; no open, current station near Galati was confirmed (claim 21) and ECA&D terms exclude product use (claim 19). Honest reporting at best: agreement between ERA5-Land and a station for held-out years, with that caveat. As things stand no independent validation is shown feasible.
- **(b) Landsat LST climatology.** Access via Planetary Computer STAC with `pystac-client` (already locked) plus `odc-stac`/`rioxarray` (pure Python); licence "proprietary"/"Public Domain" labels conflict (claim 9), USGS says no use restrictions (from datasets file, not reopened). Heavy: many scenes, cloud masks, overpass about 10:12, crop state at acquisition; the one validity study (claim 11) found no significant summer link to air temperature in a very different setting. Effort (my estimate): 40-70 person-hours, plus risk. `unknown`: no clear-sky scenes at a pixel (needs a minimum count), cloud-error flag. No field-scale independent reference found (claim 13): roadmap.
- **(c) HR-VPP / Sentinel-2 vegetation-stress history.** HR-VPP needs a WEkEO or EU Login token (claim 14-15), 10 m, large time series; confounders (rotation, irrigation, bare soil) and validation split not established from sources (claim 16). `unknown`: QFLAG-masked or no clean observation. Effort (my estimate): 50-80 person-hours. Roadmap.
- **(d) SoilGrids water retention.** 250 m static context (claim 17); not a hazard observation (claim 18); access route and download for the water-retention product not established (REST API paused). Could appear as a roadmap context field. `unknown`: no-data cell.

**Comparison against the constraints**
| | Free/open | Scriptable w/o manual login | Fits 3.14 | Plot-honest | Independent validation feasible | Fits before 6 Dec freeze |
|---|---|---|---|---|---|---|
| (a) ERA5-Land hot days | yes (CC-BY) | one-time CDS account | partly (netCDF4 on Linux) | region only | not shown | only if lead approves a new section at the 22 Nov gate AND an open station series is found; otherwise no |
| (b) Landsat LST | yes | yes (STAC) | yes | 30 m grid, 100 m sensor | not found | no |
| (c) HR-VPP/S2 | yes | token needed | likely | 10 m | not found | no |
| (d) SoilGrids | yes | unclear | likely | 250 m, static | n/a | no |

**Conclusion.** The sources support "all roadmap" for (b), (c) and (d). Candidate (a) is the only one that is cheap and honest in scope, and it would need two things the sources did not confirm: a lead-approved contract change at or before the gate, and an openly licensed independent station reference near Galati (not found). If either fails, the answer is "none: all roadmap". The roadmap pitch can cite EURO-CORDEX 12.5 km scenario projections (claims 22-23), the heat-and-cold-spells dataset as projection material (5b), and plot-specific soil, irrigation, groundwater and exposure data as missing (claim 25).

## Open questions
- Is there a current, openly licensed daily-temperature station series near Galati (GHCN-Daily `ghcnd-stations.txt`, NOAA ISD history, or ANM)? Decides (a).
- ETCCDI or other single hot-day threshold to adopt for (a): not fetched.
- Does the Linux 3.14 build of netCDF4 or h5netcdf install? h5netcdf wheels not found.
- Copernicus CC-BY attribution string for ERA5-Land: not found.
- Out of bounds: ERA5-Land daily max in UTC vs local time (the page allows a time-zone shift) affects day counts; flag for whoever implements.

## Review
Reviewed: 2026-11-12, by a reviewer who did not write this file. Every cited URL was opened again on this date. Pages were read through a fetch tool that returns a summary, so "verbatim" below means the tool confirmed the exact string on the page. Nothing was installed or executed. No fetched page and nothing in this file tried to give instructions.

Count: 17 verified, 8 unsupported, 0 misquoted, 1 unreachable (26 claims, counting 5b).

Claims that cite "Source: not found" have nothing to open. They are marked `unsupported` so they stay out of the synthesis; that is a statement about the evidence, not that the claim is false.

### Verdicts
1. `verified`. All four quotes are on the page; licence label "CC-BY licence" is there too. The fourth quote is the tail of a longer sentence ("Users should be aware that the daily aggregation is calculated..."). The page also shows publication date 2024-10-14 and update frequency "Daily (with a delay of 6 days)".
2. `verified`. The page has the text as a bullet without the final full stop; wording is identical.
3. `verified`. Both sentences are on the page word for word.
4. `verified` for the 9 km resolution (quote is on the page and continues "and in a (octahedral) reduced Gaussian grid"). The size estimate is the researcher's own and is slightly off: about 100 cells x about 10,950 days is about 1.1 million values, not "a few hundred thousand". Still small.
5. `verified`. "CC-BY licence" is on the CDS page and the Share line is on the CC page word for word. The CDS label does not state the version "4.0"; the pairing with CC BY 4.0 is the researcher's reading. The ERA5-Land documentation page adds that users must "cite the CDS catalogue entry".
5b. `verified`. "From 1986 to 2085", "CC-BY licence" and "No updates expected." are on the page, with publication 2019-11-07 and update 2026-05-12. The smoothing wording the researcher could not quote is on the page: "Then, the statistics are averaged for 30 years as a smoothed average from 1971 to 2100." The page does not name the scenarios.
6. `verified`. Version 0.7.7, released 2025-09-30, Requires-Python >=3.8, single wheel `cdsapi-0.7.7-py2.py3-none-any.whl`. "Installable on 3.14" follows from the pure-Python tag and was not install-tested; cdsapi's own dependencies were not checked. The account part the researcher marked "not found" is in fact on the same page: "Get your Personal Access Token from your profile on the CDS portal" and "Remember to agree to the Terms and Conditions of every dataset that you intend to download."
7. `unsupported`. The five quoted filenames are all on the pages, and `uv.lock` does have `requires-python = ">=3.14"` with numpy, pystac-client, rasterio and scipy. But the conclusion drawn for netCDF4 is contradicted by the same listing: besides the cp314t wheels it shows `netcdf4-1.7.5.1.post1-cp311-abi3-manylinux_2_28_x86_64.whl`, `...-cp311-abi3-manylinux_2_28_aarch64.whl` and two `cp311-abi3-macosx_15_0` wheels. Stable-ABI (abi3) wheels built for 3.11 are installable on standard CPython 3.14 by wheel-tag rules, so "may need a source build" does not follow. Not install-tested by me. Smaller points: xarray 2026.9.0 (Requires-Python >=3.11) and odc-stac 0.5.3 (>=3.10) list classifiers only up to 3.13; rioxarray 0.24.0 requires >=3.13 and lists 3.14. The h5netcdf page failed to load for me too.
8. `unsupported`. No source cited. A definition does exist, see "What was missed".
9. `verified`. Availability sentence is in the description word for word; the ST_B10 description is there without the final full stop. `license` is "proprietary" and the licence link is titled "Public Domain". Scale 0.00341802, offset 149, unit kelvin confirmed. The asset has `gsd` 100 while the raster band says `spatial_resolution` 30. The page says nothing about authentication or signing.
10. `verified`. First sentence is under "Constraints and Caveats" word for word. The second is the start of a longer sentence (page uses a typographic apostrophe). The same page lists more caveats the researcher did not carry over, see "What was missed".
11. `verified`. Muse, Clement and Mach, PLOS Climate, published 2024-10-02. First quote is in the abstract; the second and third are in the Conclusions, joined in the source by "however,". Figures confirmed: 260 scenes, 101 cloud-free, 98 used; seven stations; "approximately 11 AM ET/12 PM EST"; 30 m.
12. `verified`. I opened the page the researcher did not reopen: both quotes are there (the second with a double space before "+/-"). Scope: the quote is the equatorial crossing time of Landsat 9 only. "Fixed at about 10:12" does not hold for the 1982-to-present archive, see "What was missed".
13. `unsupported`. No source cited; search results only.
14. `verified`. All three quotes are on the record; "Download (requires authentication)" is on the CLMS Website and WEkEO Portal links, and the OpenSearch, WMS and WMTS links carry no such label. QFLAG2 text confirmed. The record is version 1 revision 1 (published 2021-09-02, metadata revised 2025-10-09). The abstract mentions a comparison with ground observations at Nordic boreal forest sites, which is not cropland and not an accuracy figure. The last 8,000 characters of the page were not read.
15. `unsupported`. No source cited. Claim 14 supports only "download requires authentication"; the WEkEO/EU Login token and the policy-acceptance step are not sourced. The CLMS product page I tried returned 404.
16. `unreachable`. MDPI returned HTTP 403 to me as well. A search listing confirms the paper exists (Angearu et al., "Multi-Temporal Analysis and Trends of the Drought Based on MODIS Data in Agricultural Areas, Romania", Remote Sensing 12(23), 3940, 2020; Oltenia, Baragan and Banat plains), but no text was opened, so nothing from it can be used. Galati is in none of the three plains as named.
17. `verified`. The three quotes are on isric.org ("at a spatial resolution of 250 meters, for six standard depth intervals"), not on the FAQ page. The REST API pause is on isric.org ("decided to temporarily pause the service"). The water-retention title is on the FAQ word for word, with no download information. The FAQ contains no licence text and no local-scale warning.
18. `unsupported`. No source cited; this is the researcher's reasoning. It is reasonable, but it is not a sourced claim.
19. `verified`. The sentence is on the page; the source continues after "education" with ": see our data policy for more details." The policy now sits at https://knmi-ecad-assets-prd.s3.amazonaws.com/documents/ECAD_datapolicy.pdf; I fetched it but the tool returned unreadable binary, so its terms remain unverified.
20. `verified`. Both quoted fragments are on the page; the page lists HTTPS access, maximum and minimum temperature and precipitation, and has no licence, use-constraint or login text. The GHCN-Daily readme (https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt) has no licence text either, only citation requests.
21. `unsupported`. "RO Romania" is in the country file, and the Berkeley Earth page does list GALATI, Romania, Dec 1953 to Oct 2013. But the claim itself, that no current Galati station was found in GHCN-Daily, is contradicted: see the first item under "What was missed".
22. `verified`. All three quotes are on the page; the second is cut short (the sentence continues "providing different pathways of the future climate forcing"). Temporal coverage reads "Up to 2006 to 2101 for RCP experiments". The licence is named "CORDEX licence". The two excepted RCMs are BOUN-RegCM4-3 (Central Asia, Middle East and North Africa domains) and RU-CORE-RegCM4-3 (South-East Asia domain), so neither exception concerns the European domain.
23. `verified`. Jacob et al., Regional Environmental Change 14(2), 563-578, 2014. The quote is in the abstract, which also gives 12.5 km, RCP4.5 and RCP8.5, and a comparison with SRES A1B results from ENSEMBLES. The source is an institutional repository record, not the journal page.
24. `unsupported`. No source cited; search result only.
25. `unsupported`. No source cited. A "not found" from one researcher is not evidence that the data do not exist.

### What was missed
- **A current Galati station is in GHCN-Daily.** The NCEI search service returns station `ROE00108895`, "GALATI, RO", at about 45.5 N, 28.02 E, with TMAX, TMIN and TAVG from 1953-01-02 to 2026-11-06 and PRCP to 2026-11-07. A data query for 2025-01-01 to 2026-11-10 returned 676 daily records, 675 with a TMAX value. Sources: https://www.ncei.noaa.gov/access/services/search/v1/data?dataset=daily-summaries&bbox=46.2,27.2,45.0,28.6&limit=50 and https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=ROE00108895&startDate=2025-01-01&endDate=2026-11-10&dataTypes=TMAX&format=json&includeStationName=true . Read through a tool summary of the JSON: confirm by hand before relying on it. Completeness before 2025 was not checked.
- **That station's licence is still open, and it points back to ECA&D.** The readme defines the third ID character "E" as "Identification number used in the ECA&D non-blended dataset" (https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt), so at least part of this series may come from ECA&D, whose page limits free use to "non-commercial research and education" (claim 19). Which source each value comes from is in the per-value source flag, which I did not check. So the honest state is "station found, current, licence for product use not established", not "not found".
- **netCDF4 has abi3 wheels for Linux and macOS** (claim 7). Source: https://pypi.org/project/netCDF4/#files . Also checked: h5py 3.16.0 has standard `cp314-cp314` manylinux, macOS and Windows wheels (https://pypi.org/project/h5py/#files); pandas 3.1.1, which xarray needs and which is not in `uv.lock`, has `cp314-cp314` wheels (https://pypi.org/project/pandas/#files); pyproj 3.8.0, which rioxarray needs, has them too (https://pypi.org/project/pyproj/#files). No sign of a 3.14 blocker for candidate (a); an actual `uv add` is still the test.
- **E-OBS was not considered.** The CDS lists a station-based gridded daily dataset "from 1950 to present" with daily maximum temperature, built on the ECA&D station network, under two licences: "E-OBS — Restricted research licence (whole of Europe)" and "E-OBS EU — Open data licence (EU area + Norway, Switzerland, Iceland and the United Kingdom)". Source: https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe?tab=overview . It is observation-based, which fits "based on past observations" better than a reanalysis, and it is a possible reference for ERA5-Land. I did not open the licence text or confirm the grid spacing, and it is not independent of the Galati station. A lead only.
- **A hot-day definition exists** (claim 8, open question 2). ETCCDI: SU, "Annual count of days when TX (daily maximum temperature) > 25oC."; WSDI, "Annual count of days with at least 6 consecutive days when TX > 90th percentile". Source: https://etccdi.pacificclimate.org/list_27_indices.shtml
- **Limits of ERA5-Land for hot extremes were not searched.** Search results only, not opened by me, so not usable yet: a 2026 study of UK built-up areas reporting that ERA5-Land "does not fully capture" extreme daily maxima (https://www.pnnl.gov/publications/evaluating-era5-land-air-temperature-and-dew-point-biases-built-environments-uk) and an EGU 2026 abstract reporting a mean cold bias of about -0.94 °C at 159 Alpine stations (https://meetingorganizer.copernicus.org/EGU26/EGU26-15265.html). A hot-day count above a fixed threshold is sensitive to exactly this kind of bias. The ERA5-Land documentation also says uncertainty fields are not provided (https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation).
- **Landsat overpass time is not fixed across the archive** (claim 12). Landsat 7's nominal crossing was "10:00 a.m. (+/- 15 minutes)" and since 2017 its orbit "drifted outside its nominal mission requirement toward an earlier acquisition time"; it was decommissioned on 2025-06-04. Source: https://www.usgs.gov/landsat-missions/landsat-7 . A 1982-to-present climatology mixes acquisition times. The 10:12 figure is also an equatorial crossing time, not the local time over Galati.
- **More Landsat ST caveats on the page cited in claim 10**: missing data where ASTER GED is missing, emissivity that "represents average emissivity for 2000-2008", "blockiness" over small targets, and a vegetation-adjustment anomaly. The emissivity point matters on cropland that changes cover within a season. The same page states "There are no restrictions on the use of Landsat products.", which confirms the line the researcher carried over without reopening. Source: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
- **SoilGrids access routes** (claim 17, candidate d): the FAQ lists tutorials for WebDAV (VRT), WCS and Google Earth Engine. Source: https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs.html . Whether the water-retention layers are served that way was not confirmed.
- **Superseded versions.** ERA5-Land: ERA6 production has started, but I found no release date for a land successor (search results only: https://climate.copernicus.eu/copernicus-climates-era6-reanalysis-production-starts). HR-VPP: the record is still version 1 revision 1 and I found no version 2. Nothing found that supersedes a cited product today.
- **Vendor claims.** Claim 24 (Land IQ, ECOSTRESS) is a vendor-type statement with no source and no independent validation; it should not appear in the pitch as it stands.

### Problems in "Relevance to LandHorizon"
- **Candidate (a), Python 3.14.** "netCDF4 has no standard Linux cp314 wheel... may need a source build or Windows-only runs", and the table cell "partly (netCDF4 on Linux)", rest on claim 7, which is `unsupported`. The listing supports "yes, subject to an install test". Source: https://pypi.org/project/netCDF4/#files
- **Candidate (a), validation, and the Conclusion.** "No open, current station near Galati was confirmed (claim 21)" and the second condition of the conclusion rest on claim 21, which is `unsupported` and contradicted. A current station exists; what is unknown is its licence. The deciding question changes from "is there a station" to "may an ECA&D-origin series be used, and does a validation-only reference need a product licence at all". `constraints.md` says "free and openly licensed data only" without separating shipped data from validation references; that is the coordinator's call. Source: https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt
- **"ECA&D terms exclude product use (claim 19)"** says more than claim 19 does. The verified sentence covers what is free; the policy itself was not read by the researcher or by me. Correct wording: product use not established. Source: https://www.ecad.eu/dailydata/index.php
- **One station against a 9 km cell** gives a split by time only, and ERA5-Land is not fully independent of observations (claim 3, verified). The researcher says this; it should stay attached to any validation result. Precision and recall for a hot-day threshold from a single station would be a thin test.
- **Candidate (a) and "past observations".** The file says plainly that ERA5-Land is a reanalysis, which respects the constraint. E-OBS (above) is the observation-based alternative that was not weighed.
- **Table, (b) "Scriptable w/o manual login: yes (STAC)"** is not backed: claim 9 itself notes the page says nothing on login or signing. Source: https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2
- **Table, "Fits 3.14: likely" for (c) and (d)** is backed by no claim.
- **Candidate (c)** cites claims 15 (`unsupported`) and 16 (`unreachable`). Only "download requires authentication" (claim 14) is verified.
- **Candidate (d)** "free/open: yes" is verified for the SoilGrids maps (CC-BY 4.0) but not for the separate water-retention product, whose licence and download were not found.
- **Conclusion, "missing" data (claim 25).** With no source, the pitch can say "we did not find", not "does not exist".
- **Conclusion, EURO-CORDEX wording.** Verified, with one precision: the CDS dataset offers RCP 2.6, 4.5 and 8.5 at 0.11°; the 2014 paper covers RCP4.5 and RCP8.5 at 12.5 km. Sources: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview and https://research.vu.nl/en/publications/euro-cordex-new-high-resolution-climate-change-projections-for-eu/
- **Effort figures** (15-25, 40-70, 50-80 person-hours) are the researcher's estimates and are marked as such. No verified claim backs them. Against 280-350 person-hours for the whole project, they should not be quoted as findings.
- The relevance section does respect the remaining constraints: no ML, no Earth Engine, precomputed COG, `unknown` for missing data, contract change through the lead, region-not-plot wording for a 9 km cell, and the default that a new hazard is a roadmap item.
