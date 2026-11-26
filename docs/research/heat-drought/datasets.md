# Which free heat and drought datasets cover Romania, at what resolution, with what access and licence? (H2 inventory)
Date: 2026-11-12
Scope: inventory and fitness facts only. Out of bounds: definitions, which indicator to build, effort, flood and ground motion. The session was interrupted by tool and usage limits, so coverage is partial: items marked "not found" or "not fetched" were not verified from a primary page. "1 ha plots per cell" figures are my own arithmetic (cell area / 10,000 m2, at about 45.7 N), not source claims. A second pass (claims 29-47, section "Second pass") was added after the first; claims 9, 12, 14, 15, 21, 23, 24, 27, 28 are superseded or narrowed there.

## Claims

### 1. Reanalysis and gridded observations
1. **Claim:** ERA5-Land is a 9 km (about 0.08 deg) hourly land reanalysis, 1950 to about 2-3 months before present, run without data assimilation. A 9 km cell is about 8,000 ha, so thousands of 1 ha plots share one cell. Reanalysis, not observation.
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
   - Quote: "The ERA5-Land HRES dataset has been produced at a resolution of 9 km, (~0.08°)"
   - Source date: 2026 (page current at fetch; exact date not shown)
   - Source type: official docs
   - Confidence: high
2. **Claim:** ERA5-Land period and temporal step.
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
   - Quote: "covers the period from January 1950 to 2-3 months before the present"; "The temporal frequency of the output is hourly"
   - Source date: 2026
   - Source type: official docs
   - Confidence: high
3. **Claim:** ERA5-Land runs without data assimilation (so soil moisture is model-driven, not corrected by observations).
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
   - Quote: "It runs without data assimilation"
   - Source date: 2026
   - Source type: official docs
   - Confidence: high
4. **Claim:** The CDS catalogue page lists ERA5-Land at 0.1 deg regridded (native 9 km), from January 1950, licence CC-BY. Access is the CDS API (account and key needed, scriptable with the `cdsapi` client; this access route is not quoted from a source here, treat as not verified).
   - Source: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview
   - Quote: "0.1° x 0.1°; Native resolution is 9 km."; "January 1950 to present"; "CC-BY licence"
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium (page summary, licence text of the CDS "Licence to use Copernicus Products" itself not retrieved)
5. **Claim:** ERA5 is 31 km, from 1940, with a daily ERA5T update about 5 days behind real time. About 96,000 ha per cell.
   - Source: https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation
   - Quote: "The ERA5 HRES atmospheric data has a resolution of 31km, 0.28125 degrees"; "covers the period from January 1940 to the present"
   - Source date: 2026
   - Source type: official docs
   - Confidence: high
6. **Claim:** CERRA (European regional reanalysis) is 5.5 km, September 1984 to present, GRIB2, CC-BY. About 3,000 ha per cell. Ensemble members are 11 km.
   - Source: https://cds.climate.copernicus.eu/datasets/reanalysis-cerra-single-levels
   - Quote: "5.5 km x 5.5 km for CERRA high-resolution reanalysis."; "From September 1984 to present"; "CC-BY licence"
   - Source date: 2026
   - Source type: official docs
   - Confidence: high (the end date of the data, as opposed to "present", was not checked)
7. **Claim:** E-OBS is daily gridded station observations, 1950 to present, with Tmean, Tmin, Tmax, precipitation, radiation, humidity, wind, pressure. Resolution is not stated on the catalogue page (about 0.1 deg is commonly quoted, not verified here). Two licences: a restricted research licence for all of Europe, and an open licence for EU + Norway, Switzerland, Iceland, UK. Romania is in the EU, so the open variant applies; I did not open the licence text to confirm commercial use.
   - Source: https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe
   - Quote: "from 1950 to present"; "E-OBS and E-OBS_EU product licences."
   - Source date: 2026-11-06 (update date shown on page)
   - Source type: official docs
   - Confidence: medium
8. **Claim:** ROCADA (Romanian national daily gridded dataset) is 0.1 deg, 1961-2013, NetCDF, available on request only, licence unknown on its catalogue record. Not open, not current: a dead end for a product pipeline.
   - Source: https://doi.pangaea.de/10.1594/PANGAEA.833627
   - Quote: "Licensing unknown: Please contact principal investigator/authors to gain access and request licensing terms (UNKNOWN)"; "The data are freely available on request in NetCDF (Network Common Data Form) format."
   - Source date: 2015 (record); fetched 2026
   - Source type: official docs (data repository record)
   - Confidence: high for 1961-2013 and licence unknown; whether a newer ROCADA version exists: not found
9. **Claim:** Copernicus (CDS) licence exact terms: not found. The licence PDF could not be read (binary) and the static URL returned 404. Do not state a wording from memory. (Narrowed by claims 29-31.)
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

### 2. Ready-made climate indicators
10. **Claim:** CDS "heat and cold spells in Europe" holds numbers of hot and cold spell days, 0.1 x 0.1 deg, 1986 to 2085 (so it mixes historical and projection), CC-BY. A 0.1 deg cell is about 8,800 ha. Page title found at the sis-heat-and-cold-spells slug.
    - Source: https://cds.climate.copernicus.eu/datasets/sis-heat-and-cold-spells
    - Quote: "The dataset contains the number of hot and cold spell days using different European-wide and national/regional definitions"; "From 1986 to 2085"; "CC-BY licence"
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium (which years are historical versus projected was not checked)
11. **Claim:** The UTCI dataset (ERA5-HEAT) is 0.25 deg, hourly with daily to yearly statistics, January 1940 to near real time, licence "Licence to use Copernicus Products". It is derived from ERA5, so cells are about 28 km (about 60,000 ha).
    - Source: https://cds.climate.copernicus.eu/datasets/derived-utci-historical
    - Quote: "From January 1940 to near real time for the most recent version."; "Licence to use Copernicus Products"
    - Source date: 2026
    - Source type: official docs
    - Confidence: high
12. **Claim:** Agroclimatic indicators on CDS and the European Climate Data Explorer: not found (not fetched).
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 3. Drought indicators
13. **Claim:** SPEIbase v2.11 is global, 0.5 deg, monthly, January 1901 to December 2024, scales 1-48 months, Open Database License with mandatory attribution. A 0.5 deg cell is about 200,000 ha: regional context only.
    - Source: https://spei.csic.es/database.html
    - Quote: "with a 0.5 degrees spatial resolution and a monthly time resolution."; "The Global 0.5° gridded SPEI dataset is made available under the Open Database License."; "You must attribute any public use of the database."
    - Source date: 2026 (v2.11, CRU TS 4.09 to Dec 2024)
    - Source type: official docs
    - Confidence: high
14. **Claim:** The EDO / GDO site offers indicator downloads, WMS and WCS services and a JRC Data Catalogue collection; SPEI is described as "based on ERA5". The page itself does not give the resolution, period or licence of SPI, soil-moisture anomaly, fAPAR anomaly or CDI, and the CDI factsheet URL returned 404. Their resolution, period and licence: not found. (Narrowed by claims 32-34.)
    - Source: https://drought.emergency.copernicus.eu/
    - Quote: "based on ERA5 data" (as reported from the page summary; the page also links "Download indicators", WMS, WCS and the JRC catalogue collection data.jrc.ec.europa.eu/collection/drought)
    - Source date: 2026
    - Source type: official docs
    - Confidence: low
15. **Claim:** SPEI Global Drought Monitor, JRC European Drought Risk Atlas data: not found (not fetched).
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 4. Satellite land-surface temperature (LST is not air temperature, clear-sky only)
16. **Claim:** MOD11A1 v061 (Terra MODIS daily LST) is 1000 m, daily, 2000-02-24 to present, "openly shared, without restriction" under EOSDIS citation guidance. A 1 km cell is about 100 ha. Access via NASA Earthdata (login required; scriptable). Overpass time and the clear-sky limit are not on this page.
    - Source: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod11a1-061
    - Quote: "This dataset is openly shared, without restriction, in accordance with the EOSDIS Data Use and Citation Guidance."; "2000-02-24 to Present"
    - Source date: 2026
    - Source type: official docs
    - Confidence: high for resolution, period and licence
17. **Claim:** ECOSTRESS L2T LSTE v002 is 70 m, 2018-07-09 to present, covers only 52 N to 52 S, irregular revisit ("Varies"), with data gaps. Galati (about 45.7 N) is inside 52 N. One 70 m cell is about 0.5 ha.
    - Source: https://www.earthdata.nasa.gov/data/catalog/lpcloud-eco-l2t-lste-002
    - Quote: "70 Meters x 70 Meters"; "collects data globally between 52° N and 52° S latitudes"; "2018-07-09 to Present"
    - Source date: 2026
    - Source type: official docs
    - Confidence: high
18. **Claim:** Landsat Collection 2 surface temperature is generated at 30 m; the TIRS bands are 100 m ground sampling distance; revisit 16 days per satellite, equatorial crossing about 10:12 a.m.; USGS Landsat has no use restrictions. The statement that the 100 m thermal data are resampled to 30 m was NOT found on a USGS page I could open: it comes only from a preprint snippet in search results (arXiv 2603.29478, not opened), so treat "resampled" as unverified.
    - Source: https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-9-olitirs-collection-2-level-2
    - Quote: "generated at the Earth Resources Observation and Science (EROS) Center at a 30-meter spatial resolution."
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
19. **Claim:** Landsat 9 TIRS ground sampling distance and revisit.
    - Source: https://www.usgs.gov/landsat-missions/landsat-9
    - Quote: "TIRS provides two spectral bands with a maximum ground sampling distance, both in-track and cross track, of 100 m (328 ft) for both bands."; "Has a 16-day repeat cycle with an equatorial crossing time of 10:12 a.m. +/- 5 minutes"
    - Source date: 2026
    - Source type: official docs
    - Confidence: high
20. **Claim:** USGS warns of a known cloud error in the Landsat surface temperature product, and has an open data policy.
    - Source: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
    - Quote: "There are no restrictions on the use of Landsat products."
    - Source date: 2026
    - Source type: official docs
    - Confidence: high (cloud-error quote is on the EROS page in claim 18: "A known error exists in the Landsat Surface Temperature retrievals relative to clouds and possibly cloud shadows.")
21. **Claim:** VIIRS LST, Sentinel-3 SLSTR LST, MYD11 / MOD21, CLMS LST, Planetary Computer / AWS / CDSE routes: not found (not fetched). (Narrowed by claims 40-41.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 5. Vegetation stress
22. **Claim:** NOAA STAR VHI is 4 km, 7-day composite, 1981 to present, FTP download, but "experimental use only" and not an official operational product (a licence concern for a product; about 1,600 ha per cell).
    - Source: https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/index.php
    - Quote: "The data and images have 4 km spatial and 7-day composite temporal resolution."; "are provided for experimental use only and are not official operational NOAA products."
    - Source date: 2026
    - Source type: official docs
    - Confidence: high
23. **Claim:** HR-VPP, Sentinel-2 NDVI / NDMI anomalies, FAO ASIS, published confounder studies: not found (the CLMS page timed out; nothing else fetched). (Narrowed by claims 35-36.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 6. Soil and water context
24. **Claim:** SoilGrids, ESDAC soil hydraulic maps, irrigation maps, groundwater: not found (SoilGrids page returned only a title). (Narrowed by claims 42-43.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 7. Projections
25. **Claim:** NEX-GDDP-CMIP6 is 0.25 deg (25 km, about 62,000 ha per cell), daily, bias-corrected downscaled CMIP6, on AWS S3 without login, and is CC0 since September 2022.
    - Source: https://registry.opendata.aws/nex-gddp-cmip6/
    - Quote: "all NEX-GDDP-CMIP6 outputs are made available under a blanket Creative Commons Zero license (CC0)"
    - Source date: 2022 (licence change); fetched 2026
    - Source type: official docs
    - Confidence: high for licence; resolution from https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6 : "Latitude Resolution: 0.25 degrees (25 km)"
26. **Claim:** CHELSA offers daily (1941-2025), monthly (1979-2021), drought-index (1980-2018) and climatology / bioclim (1981-2010 to 2071-2100) products made with a "CHELSA downscaling model". The about 1 km resolution and the licence were not stated on the page I opened. Downscaled from coarser reanalysis, so 1 km is a grid spacing, not new plot-scale information.
    - Source: https://chelsa-climate.org/
    - Quote: "generated with the CHELSA downscaling model"
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium
27. **Claim:** EURO-CORDEX, CMIP6 on CDS, Interactive Climate Atlas: not found (not fetched). (Narrowed by claims 44-45.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### 8. Forecasts
28. **Claim:** C3S seasonal forecasts and EDO drought forecasts: not found (not fetched). (Narrowed by claim 46.)
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

### Second pass (added 2026-11-12)

#### Copernicus CDS licence
29. **Claim:** The "Licence to use Copernicus Products" on the CDS, ADS and EWDS was replaced by the Creative Commons Attribution licence (CC-BY) on 2 July 2025. Dataset pages seen in this file (ERA5-Land, CERRA, heat and cold spells, seasonal) now show "CC-BY licence", but the UTCI page (claim 11) still showed the old name when fetched, and a forum user reported older licences in some STAC metadata.
   - Source: https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464
   - Quote: not found as a verbatim sentence (the page was read through a summarising tool, which paraphrased: "replaced by the Creative Commons Attribution License (CC-BY)", effective 2 July 2025). Do not use this claim until a reviewer opens the page and copies the sentence.
   - Source date: 2025-07
   - Source type: official docs (ECMWF support forum announcement)
   - Confidence: low
30. **Claim:** CC BY 4.0 allows commercial use and redistribution of the material and of adaptations, with attribution. This is the licence text for any CDS dataset that is labelled CC-BY.
   - Source: https://creativecommons.org/licenses/by/4.0/
   - Quote: "copy and redistribute the material in any medium or format for any purpose, even commercially."; "remix, transform, and build upon the material for any purpose, even commercially."; "You must give appropriate credit, provide a link to the license, and indicate if changes were made."
   - Source date: 2026 (page current; licence version 4.0 is from 2013)
   - Source type: official docs
   - Confidence: high
31. **Claim:** The exact old Copernicus licence wording and the per-dataset CDS attribution text were not retrieved from a page I opened (the licence PDF is binary, the forum post gives no fixed text and points to each dataset's "References" section). Exact attribution string: not found.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

#### EDO / Copernicus drought products
32. **Claim:** EDO is run by the JRC; EDO data "can be freely downloaded". Resolution and licence are not on that page, which links to a separate "Copyright and licenses" page that I did not open.
   - Source: https://www.copernicus.eu/en/node/2672
   - Quote: "The European drought observatory (EDO) is a service run by the European Commission's Joint Research Centre."; "These data can be freely downloaded for offline analysis."
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
33. **Claim:** CDI v4 (about 5 km at the Equator, built from SPI, soil moisture anomaly and fAPAR anomaly), SPI at 1/24 degree, download as GeoTIFF / NetCDF / WMS from the JRC catalogue. NOT verified by me: the factsheet PDF (https://drought.emergency.copernicus.eu/data/factsheets/factsheet_combinedDroughtIndicator_v4.pdf) came back as unreadable binary and the JRC catalogue page was rejected; the details come from a search-result summary only.
   - Source: not found (not opened)
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low
34. **Claim:** EDO licence for CDI, SPI, soil-moisture and fAPAR anomalies, and exact period of each: not found. SPEIbase (claim 13) is the only drought-index licence I verified.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

#### Field-scale vegetation
35. **Claim:** CLMS HR-VPP Plant Phenology Index is 10 m on the Sentinel-2 tiling grid, October 2016 to today with daily updates; CLMS products follow "full, open and free access" with a duty to inform the public of the source and to state modifications. Download needs authentication (CLMS website or WEkEO); OpenSearch, WMTS and WMS endpoints are listed.
   - Source: https://sdi.eea.europa.eu/catalogue/copernicus/api/records/65f095af-5225-490b-8a29-4500d4c31b8a
   - Quote: "10 x 10m resolution, in UTM/WGS84 projection corresponding to the Sentinel-2 tiling grid"; "for the period from October 2016 until today, with daily updates"; "The Copernicus land monitoring products and services are made available on a principle of full, open and free access"
   - Source date: 2021-09 (product version) ; fetched 2026
   - Source type: official docs (EEA catalogue record)
   - Confidence: high
36. **Claim:** Sentinel-2 L2A access and licence, MODIS / VIIRS vegetation indices, FAO ASIS, published agricultural-drought validation and confounders (crop rotation, irrigation, bare soil): not found. The Sentinel data access page returned 404.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

#### Satellite LST, remaining
37. **Claim:** VIIRS (Suomi NPP) daily LST VNP21A1D v002 is 1 km (resampled from native 750 m), 2012-01-17 to present, daily, "openly shared, without restriction". Delivery of Suomi NPP VIIRS products ceased on 2 November 2026 and the page recommends VJ221A1D or VJ121A1D (NOAA-20), so a pipeline should not depend on the VNP series going forward.
   - Source: https://www.earthdata.nasa.gov/data/catalog/lpcloud-vnp21a1d-002
   - Quote: "derived through resampling the native 750 meter VIIRS resolution"; "ceased on November 2, 2026 (2026/306)"; "is openly shared, without restriction, in accordance with the EOSDIS Data Use and Citation Guidance"
   - Source date: 2026-11
   - Source type: official docs
   - Confidence: medium (quotes come via a summarising tool that returned them in quotation marks; a reviewer should recheck the exact words)
38. **Claim:** MOD21A1D v061 (MODIS temperature-emissivity separation LST) is 1 km, daily, 2000-02-24 to present, same EOSDIS open-use statement as MOD11A1.
   - Source: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod21a1d-061
   - Quote: "2000-02-24 to Present"; "is openly shared, without restriction"
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
39. **Claim:** Sentinel-3 SLSTR LST (1 km), any CLMS LST product, Planetary Computer / AWS / CDSE routes and the overpass times of MODIS and VIIRS: not found (CDSE Sentinel-3 page returned 404).
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

#### Soil context
40. **Claim:** SoilGrids is 250 m, six depth intervals, under CC-BY 4.0; the REST API is temporarily paused with "more stable ways" via the ISRIC docs; water retention at 100, 330 and 15 000 cm suction is a separate WoSIS-based product (Turek et al. 2023). A 250 m cell is 6.25 ha.
   - Source: https://www.isric.org/explore/soilgrids
   - Quote: "The SoilGrids maps are publicly available on the SoilGrids website under the CC-BY 4.0 License."
   - Source date: 2026
   - Source type: official docs
   - Confidence: high (250 m wording from https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs.html: "set of global maps of soil properties for six depth intervals at 250 m spatial resolution")
41. **Claim:** ESDAC soil hydraulic / available water capacity maps (page returned 404), irrigation extent maps, groundwater: not found.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

#### Projections and forecasts
42. **Claim:** CORDEX on the CDS: European domain 0.11 deg (about 12 km), RCP 2.6, 4.5 and 8.5 experiments up to 2101, historical up to 2010; commercial use allowed per the CORDEX licence, with exceptions for two RegCM4-3 simulations (BOUN, RU-CORE). Bias-adjusted variants: not found.
   - Source: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels
   - Quote: "European domain: 0.11°x0.11°"; "These scenarios are the RCP 2.6, 4.5 and 8.5 scenarios"; "Precise terms of use are provided in the CORDEX licence."
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium (quotes via summarising tool, recheck wording)
43. **Claim:** The Copernicus Interactive Climate Atlas page returned only its title; resolution, licence and download: not found. CMIP6 on the CDS: not found.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low
44. **Claim:** C3S seasonal forecasts on the CDS are 1 deg x 1 deg, hindcasts 1993-2016 and forecasts 2017 to present, released monthly, CC-BY plus an "Additional licence to use non European contributions". 1 deg is about 8 million m2... i.e. about 600,000 ha per cell: regional context only.
   - Source: https://cds.climate.copernicus.eu/datasets/seasonal-original-single-levels
   - Quote: "1° x 1°"; "1993 to 2016 (hindcasts); 2017 to present (forecasts)"; "Additional licence to use non European contributions"
   - Source date: 2026
   - Source type: official docs
   - Confidence: medium
45. **Claim:** EDO drought forecasts: not found.
   - Source: not found
   - Quote: not found
   - Source date: not found
   - Source type: not found
   - Confidence: low

## Relevance to LandHorizon
- **Coverage versus a plot:** every dataset with a verified resolution is far coarser than a 1 ha plot except ECOSTRESS (about 0.5 ha cells, but irregular, clear-sky and sparse), Landsat (30 m grid, 100 m sensor) and HR-VPP (10 m). ERA5-Land, CERRA, E-OBS, heat-spell days, SPEIbase, VHI, NEX-GDDP and the seasonal forecasts describe the region or neighbourhood, not the plot, and should be presented that way. MODIS / VIIRS LST at 1 km is about 100 ha. SoilGrids at 250 m is 6.25 ha, so a plot gets 0 to a few cells.
- **Licence:** CC-BY (ERA5-Land, CERRA, heat-spell days, seasonal, SoilGrids), ODbL with attribution (SPEIbase), CC0 (NEX-GDDP), no restrictions (MODIS, VIIRS, Landsat) and "full, open and free" with source credit (CLMS HR-VPP) look usable in a product; a derived raster needs the attribution, and CC BY 4.0 explicitly allows commercial redistribution and adaptation (claim 30). E-OBS needs the open "E-OBS_EU" variant and a check of its text. ROCADA is a dead end (on request, licence unknown, ends 2013). NOAA VHI is "experimental use only". EDO products: licence not found. The exact CDS attribution string: not found.
- **Access:** CDS needs an account and key but is scriptable; NASA Earthdata needs a login but is scriptable; NEX-GDDP on AWS S3 is anonymous; HR-VPP download needs CLMS or WEkEO authentication. None needs Earth Engine in what I verified. The size of a one-region extract: not found for all datasets (a Galati box is a handful of cells for the coarse ones).
- **Pipeline:** do not build on Suomi NPP VIIRS LST (delivery ceased 2 Nov 2026).
- **Cost and compute:** the coarse gridded sets are tiny for one region; MODIS / Landsat / ECOSTRESS / HR-VPP time series would be the heavy part: not found.
- **Still not covered:** EDO resolution, period and licence (verified); Sentinel-2 access; SLSTR; CLMS LST; ESDAC; irrigation; groundwater; CMIP6 and the Climate Atlas; EDO forecasts; agroclimatic indicators; the SPEI Global Drought Monitor; the Drought Risk Atlas; published validation and confounder studies.

## Open questions
- What are the exact CDS "Licence to use Copernicus Products" terms (the licence PDF was not readable) and the per-dataset CC-BY attribution text? Claim 29 needs a reviewer to copy a verbatim sentence.
- Resolution, period and licence of the EDO products (SPI, CDI, soil moisture anomaly, fAPAR anomaly), and whether JRC data are redistributable: still not verified from a readable page.
- Is the Landsat 100 m to 30 m resampling stated in the USGS Level-2 product guide (DFCB)?
- Is E-OBS_EU open licence text compatible with commercial redistribution?
- Claim 44 contains a clumsy area remark ("8 million m2..."); only "about 600,000 ha" is meant (1 deg x 1 deg is roughly 8,000 km2 = 800,000 ha at this latitude, so 600,000 ha is rough and should be recomputed).
- Out of bounds, one line: the definitions of heatwave and drought are covered by another researcher.

## Review
Reviewed: 2026-11-12, by a reviewer who did not write this file.

How this was checked: every cited URL was opened on 2026-11-12. Pages were read through a fetch tool that caps a quoted span at about 125 characters, so long quotes were confirmed either as an exact-string yes/no check or in consecutive segments. No fetched page and nothing in this file contained instructions addressed to the reader; none were followed.

Convention for the "not found" entries: they cite no source and no quote, so there is nothing to open. They get `unsupported`, meaning "a gap marker, not a fact, not usable in a synthesis". It does not mean the researcher was wrong to write "not found".

Counts: 29 `verified`, 15 `unsupported` (all gap markers), 1 `unreachable`, 0 `misquoted`.

### Verdicts
1. `verified` — The quoted sentence is on the page (it continues "and in a (octahedral) reduced Gaussian grid"). The page was last modified 2025-09-29, not 2026. The hectare figure is the researcher's arithmetic and is right (81 km2).
2. `verified` — Both quotes present. See "Missed" item 1: the 2-3 months is only the consolidated release.
3. `verified` — Quote present.
4. `verified` — All three quotes present; the page also gives publication date 2019-07-12 and update frequency "Daily". The `cdsapi` access route is not on this page, as the researcher says; see "Missed" item 2.
5. `verified` — Both quotes present. The ERA5T part is not in the quote but is on the page: "daily updates for ERA5T are available about 5 days behind real time".
6. `verified` — All three quotes present; the page also has "11 km x 11 km for CERRA ensemble members" and "GRIB2". "To present" is the page's wording but probably not the real end of the data: see "Missed" item 3.
7. `verified` — Both quotes present; update date 2026-11-06, the variable list and the two licence labels ("Restricted research licence (whole of Europe)", "Open data licence (EU area + Norway, Switzerland, Iceland and the United Kingdom)") confirmed. No grid spacing on the page and no licence text; I could not retrieve the E-OBS_EU licence text either, so commercial use stays unconfirmed.
8. `verified` — Both quotes present, plus "at a spatial resolution of 0.1°" and "covering the interval 1961-2013". The record says "Published: 2014-06-25", so the source date is 2014, not 2015. "Dead end" is the researcher's judgement, not the source's.
9. `unsupported` — Gap marker, no source. Narrowed by 29-30, which are verified.
10. `verified` — All three quotes present, "0.1° x 0.1°" also present. Important caveat the claim understates: see "Missed" item 4. The real title is "Heat waves and cold spells in Europe derived from climate projections".
11. `verified` — Both quotes present, plus "0.25° x 0.25°" and "Hourly data, with additional daily, monthly, seasonal and yearly statistics." The page still showed the old licence name on 2026-11-12. At 45.7 N a 0.25 deg cell is about 54,000 ha, not 60,000.
12. `unsupported` — Gap marker, no source.
13. `verified` — All three quotes present; v2.11, "January 1901 to December 2024", "time-scales between 1 and 48 months" and CRU TS 4.09 confirmed. The page's "SPEIbase details" section still names CRU TS 4.03, an inconsistency on the source itself.
14. `verified` — "based on ERA5 data" is on the page, in a sentence about SPEI. "Download indicators", "WMS Service", "WCS Service" and the JRC Data Catalogue link are there. No resolution, period or licence for any indicator, as the researcher says.
15. `unsupported` — Gap marker, no source.
16. `verified` — Both quotes present, plus "1000 Meters x 1000 Meters" and "1 Day". Two details are not from this page: "login required; scriptable" is not stated on it, and the page does mention clear-sky ("the criteria for clear-sky are met", layers "Day_view_time" and "Night_view_time"), so "the clear-sky limit is not on this page" is slightly off. See "Missed" item 5 on Terra.
17. `verified` — All three quotes present, temporal resolution "Varies" confirmed. The Known Issues section lists acquisition gaps (2019, 2020) and that the product "was generated without the lst_err layer" from 2025-12-16 to 2026-06-10.
18. `verified` — Exact sentence present: "The Surface Temperature products are generated at the Earth Resources Observation and Science (EROS) Center at a 30-meter spatial resolution." The page has no revisit information; that part rests on claim 19. On resampling see "Missed" item 6.
19. `verified` — Both quotes present, character for character.
20. `verified` — "There are no restrictions on the use of Landsat products." is on the cited page. That page's cloud sentence reads "A known error exists in the surface temperature retrievals relative to clouds and possibly cloud shadows."; the wording in the confidence line is on the EROS page of claim 18, as stated.
21. `unsupported` — Gap marker, no source. The cross-reference is wrong: it is claims 37-39, not 40-41.
22. `verified` — First quote present; the second is present as "Data and images displayed on STAR sites are provided for experimental use only and are not official operational NOAA products." "1981 to the present" is in the body text (the menu says "since 1982" for the blended product). "FTP download" is not stated in the text; there is only a "Download Data" link to `vh_ftp.php`. The "experimental use" line is a disclaimer about operational status, not licence text; calling it a licence concern is the researcher's reading.
23. `unsupported` — Gap marker, no source.
24. `unsupported` — Gap marker, no source. The cross-reference is wrong: it is claims 40-41, not 42-43.
25. `verified` — CC0 quote present on the AWS page, with "No AWS account required", "daily" and "bias-corrected". "Latitude Resolution: 0.25 degrees (25 km)" and "Temporal Resolution: daily" present on the NCCS page. At 45.7 N the cell is about 54,000 ha; 62,000 ha is the 25 km x 25 km figure.
26. `verified` — Quote present ("CHELSA-daily is a global, kilometer-scale climate dataset generated with the CHELSA downscaling model."). Year ranges confirmed (daily to 2025-08-29, status "active (incomplete)"). No numeric resolution and no licence on the page, as stated. The last sentence of the claim is the researcher's interpretation.
27. `unsupported` — Gap marker, no source. The cross-reference is wrong: it is claims 42-43, not 44-45.
28. `unsupported` — Gap marker, no source. The cross-reference is wrong: it is claims 44-45; there is no claim 46.
29. `verified` — I opened the page. The researcher's paraphrase is not the source's wording, so use these verbatim segments instead. First post, ECMWF Support, 2025-06-13: "on Wednesday 2nd July 2025" ... "in the Climate Data Store (CDS), Atmosphere Data Store (ADS) and the CEMS Early Warning Data Store (EWDS)" ... "will be replaced with the Creative Commons Attribution License (CC-BY)". Confirmation post, 2025-07-02: "we can confirm that the replacement of the Licence to use Copernicus Products with the" "Creative Commons Attribution Licence (CC-BY) was successfully implemented." The STAC remark is there (a user, 2025-07-17: "I noticed that the STAC metadata for some datasets still reflects the older licenses."), but ECMWF Support answered the same day "I’m not seeing what you are seeing for the 2 datasets you listed", which the claim leaves out. The UTCI page did still show the old name when I fetched it.
30. `verified` — All three quotes are on the deed.
31. `unsupported` — Gap marker, no source. The forum posts in claim 29 do say "please refer to the References section on each dataset entry"; no fixed attribution string was found by me either.
32. `verified` — Both sentences present (the page uses a curly apostrophe in "Commission’s"). No page date is shown. The linked "Copyright and licences" page says nothing about EDO or CEMS data: see "Missed" item 7.
33. `unreachable` — I tried the factsheet URL named in the claim: it came back as an unreadable binary PDF. `data.jrc.ec.europa.eu/collection/drought` answered "The requested URL was rejected." None of the figures in this claim (about 5 km, 1/24 degree, formats) may be used.
34. `unsupported` — Gap marker, no source. I could not find the EDO licence either.
35. `verified` — All three quotes present (title: "High Resolution Vegetation Phenology and Productivity: Plant Phenology Index (raster 10m) version 1 revision 1, Sep. 2021"). Also present: "users shall inform the public of the source of these products and services", "the user shall clearly state this", and "Download (requires authentication)" on the CLMS and WEkEO links. Metadata last revised 2025-10-09.
36. `unsupported` — Gap marker, no source.
37. `verified` — All three quotes present, plus "1000 Meters x 1000 Meters", "1 Day", "2012-01-17 to Present". One error: the claim labels both replacements "(NOAA-20)". The page does not name the satellites, and VJ221A1D, which the page lists first, is NOAA-21: see "Missed" item 8.
38. `verified` — Both quotes present, plus "1000 Meters x 1000 Meters" and "1 Day". The page warns of "extreme high temperature outliers" in MxD21 and that "values for the contaminated pixels are retained in the output products", which the claim leaves out.
39. `unsupported` — Gap marker, no source.
40. `verified` — Licence sentence present on the ISRIC page, with "a spatial resolution of 250 meters", "for six standard depth intervals", "have decided to temporarily pause the service" and "alternative, more stable ways to access SoilGrids". The 250 m quote is on the FAQ page. The water-retention detail is not on the ISRIC page at all; it is only in the reference list of the FAQ page ("volumetric water retention at 100, 330 and 15 000 cm suction", Turek et al.), so cite the FAQ for it. ISRIC adds "we cannot provide an estimated timeline for when the service will be restored".
41. `unsupported` — Gap marker, no source.
42. `verified` — All three quotes present. "Up to 1948 to 2010 for historical experiments", "Up to 2006 to 2101 for RCP experiments" and "The data can be used for commercial purposes (unrestricted use) with the exception of the simulations from the following RCMs" confirmed; the two exceptions are for non-European domains. The page also says the typical periods are 1950-2005 and 2006-2100. The Licence field reads "CORDEX licence", not CC-BY. No mention of bias-adjusted data.
43. `unsupported` — Gap marker, no source.
44. `verified` — All three quotes present; releases are "once per month on the 6th at 12UTC for ECMWF" and on the 10th for the other centres. The area arithmetic in the claim is wrong and must not be reused: 1 deg x 1 deg at 45.7 N is about 111 km x 78 km, about 8,600 km2, about 860,000 ha (and about 8.6 billion m2, not 8 million).
45. `unsupported` — Gap marker, no source.

### What the researcher missed
1. **ERA5-Land has a near-real-time stream.** The same page as claims 1-3 says "daily updates for ERA5-Land-T are available about 5 days behind real time" and that the stream "delivers non-checked close to Near-Real-Time (NRT) daily updates", replaced by final data about two months later. The 2-3 month lag in claims 1-2 is only the consolidated release. https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
2. **CDS access needs one manual step per dataset.** The API guide requires an account and a personal access token in `$HOME/.cdsapirc`, the `cdsapi` client, and accepting each dataset's terms: "This step must be done manually from the dataset page". Scriptable after that. The token is a secret and must stay out of git. https://cds.climate.copernicus.eu/how-to-api
3. **CERRA "to present" is not present.** ECMWF Support announced on 2025-01-23 that data "for the period from 1 July 2021 to 31 July 2022 are now available"; before that the record stopped at June 2021. In a related thread a user reported on 2025-06-20 that "the last date available at the CDS is 202308", Support's plan "to catch up with the real time in Q2/2025" slipped to Q3 2025, and CERRA-Land was reported still ending April 2021. I could not establish the end date as of today; it has to be checked on the download form before CERRA is called current. https://forum.ecmwf.int/t/additional-cerra-data-for-the-period-from-july-2021-to-july-2022-now-available-on-the-cds/10954 and https://forum.ecmwf.int/t/new-cerra-data-still-according-to-plan/7958
4. **The heat and cold spell dataset is model output only, not observations.** The page says the statistics are "based on a bias-adjusted EURO-CORDEX dataset", "averaged for 30 years as a smoothed average from 1971 to 2100", which "results in a timeseries covering the period from 1986 to 2085", then "averaged for the model ensemble". So "1986" is a 30-year model mean, not an observed year. Saying it "mixes historical and projection" undersells this. The page names no scenarios. https://cds.climate.copernicus.eu/datasets/sis-heat-and-cold-spells
5. **Terra and Aqua MODIS are ending.** NASA Earthdata (alert of 2025-05-02) says that in late 2026 or early 2027 Terra and Aqua "will begin shutting down operations", that both are "drifting out of their designed orbits" which changes crossing times and may affect the data, and it points users to VIIRS. This touches claims 16 and 38: the archive stays usable, but MOD11A1 and MOD21A1D will stop growing and the recent years are affected by the drift. Neither product page carries this notice. https://www.earthdata.nasa.gov/data/alerts-outages/transition-from-modis-viirs
6. **Landsat resampling is on a USGS page** (answers the third open question and the "unverified" note in claim 18). The band table lists TIRS bands 10 and 11 as "100 (resampled to 30)*" with the footnote "* Indicates that acquired data are resampled for Level-1 product processing." https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites
7. **The EDO licence is not on the Copernicus "Copyright and licences" page** that claim 32 points to. That page has no text on EDO or CEMS data, only on trade marks. The EDO licence is still not found by anyone. https://www.copernicus.eu/en/access-data/copyright-and-licences
8. **The VIIRS replacement has a short record.** VJ221A1D is from "NOAA-21 (JPSS-2)" and its temporal extent is "2023-02-10 to Present". A long 1 km LST series therefore needs the Suomi NPP archive (2012 to 2 Nov 2026) or MODIS for the past, plus a NOAA-20 or NOAA-21 product going forward. I did not open the VJ121A1D page. https://www.earthdata.nasa.gov/data/catalog/lpcloud-vj221a1d-002
9. **Numbering.** The scope line says "claims 29-47" but the file ends at claim 45, and four cross-references point to the wrong numbers (noted at claims 21, 24, 27, 28).
10. **The heading "LST is not air temperature, clear-sky only" has no claim behind it.** The MOD11A1 page supports the clear-sky part ("the criteria for clear-sky are met"); the "not air temperature" part has no source in this file. https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod11a1-061

### Problems in "Relevance to LandHorizon"
- **Access is asserted without a verified claim.** "CDS ... is scriptable" and "NASA Earthdata needs a login but is scriptable" are not backed by any quote in the file (claims 4 and 16 say so themselves). CDS is confirmed by "Missed" item 2, with the manual licence step, which matters under the constraint that manual-login sources cost team time. Earthdata login and scripting remain unverified. Whether `cdsapi` or an Earthdata client installs on Python 3.14 was not checked.
- **Licence list drops two conditions.** The seasonal forecasts are CC-BY plus an "Additional licence to use non European contributions" (claim 44), whose text nobody opened, so they cannot be listed as plainly usable in a product. UTCI is left out of the list and still showed the old licence name. CORDEX is under its own "CORDEX licence", not CC-BY, and is missing from the list.
- **"Past observations" constraint.** The product is a screening indicator based on past observations. The heat-spell days (item 4), NEX-GDDP, CORDEX and the seasonal forecasts are model projections or forecasts, and ERA5, ERA5-Land, CERRA and UTCI are reanalysis. The coverage bullet lists heat-spell days next to E-OBS and SPEIbase without saying so. Only E-OBS, SPEIbase (station-based), the satellite LST and vegetation products count as observations.
- **Plot-scale exceptions are thinner than they read.** Landsat thermal is a 100 m sensor resampled to 30 m (item 6), so a plot of 1 ha or less holds about one independent thermal sample. HR-VPP at 10 m is a vegetation index, not a heat or drought indicator, and the confounder question (crop rotation, irrigation, bare soil) is a "not found" in claim 36. Neither is evidence of a plot-level heat or drought signal.
- **Pipeline bullet is incomplete.** Besides Suomi NPP, Terra and Aqua MODIS are shutting down from late 2026 or early 2027 (item 5), and CERRA may end well before today (item 3).
- **Missing data.** Clear-sky LST and ECOSTRESS acquisition gaps mean many plot-dates have no value. The section does not say these must be reported as `unknown`, which the constraints require.
- **Scope default not stated.** The constraints rate a new hazard as out of scope after the 22 Nov gate, a roadmap item by default. The section does not say this; nothing in it contradicts it either, since effort is declared out of bounds.
- **Wrong arithmetic stays out.** The 600,000 ha figure in claim 44 is wrong (about 860,000 ha); the relevance text does not use it.
