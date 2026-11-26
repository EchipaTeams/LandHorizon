# Can Google Flood Hub or GloFAS (v4, v5) serve as a modelled flood-hazard layer for plot-level screening in Galati?
Date: 2026-11-11
Scope: Google Flood Hub / Flood Forecasting API / Google flood datasets; GloFAS forecasts, reanalysis, return-period thresholds, and the global JRC/CEMS river flood hazard maps (as GloFAS's static-hazard companion). Out of bounds: EFAS, European-domain JRC maps, Romanian national maps, running our own hydrodynamic model, ML surrogates, observed (Sentinel-1/GFM) mapping.

Method note: pages were read through a fetch tool that summarises pages. Quotes below are the strings that tool returned as verbatim; the CEMS news site and some PDFs (React app / compressed PDF) could not be read, so several GloFAS facts come from ECMWF Confluence wiki pages and the Early Warning Data Store (EWDS). A reviewer should re-open the quotes. No prompt-injection attempts were seen in fetched content.

## Claims

### A. GloFAS: what the products are
1. **Claim:** The GloFAS "historical" product is a daily river-discharge reanalysis (m3/s per river grid cell at 0.05 deg, ~5 km), not an inundation map. v5.0 is listed as the operational version.
   - Source: https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview
   - Quote: "Operational version - GloFAS v5.0 released 2026-07-15." and "0.05° x 0.05° for version 5.0 and version 4.0"
   - Source date: page updated 2026-11-11 (as shown on the page)
   - Source type: official docs
   - Confidence: high
2. **Claim:** The v4.0 reanalysis announcement describes the variable as discharge in m3/s on a 0.05 deg grid.
   - Source: search-result snippet of the CEMS v4.0 reanalysis announcement (https://global-flood.emergency.copernicus.eu/news/113-glofas-v34-release-and-glofas-v40-hydrological-reanalysis-dataset-announcement/); page itself not readable (React app). Treated as low confidence.
   - Quote: "daily maps of discharge (in m3/s) with quasi global (+90,-60,-180,180) extent at 0.05 degree (~5km) grid resolution"
   - Source date: 2023
   - Source type: official docs (not opened by me)
   - Confidence: low
3. **Claim:** GloFAS forecasts and reforecasts are also discharge, run on the same river network; reforecast period "From 2003-03-27 to real time" in v5; new return-period thresholds come from a 1980-2025 climatology. (Static return-period discharge thresholds are the "hazard" GloFAS itself publishes; they are discharge, not depth.)
   - Source: https://confluence.ecmwf.int/x/38QHIQ (ECMWF Confluence, "Upcoming GloFAS release v5" placeholder, old version)
   - Quote: "From 2003-03-27 to real time" and "new return period thresholds" based on a "climatology from 1980 – 2025"
   - Source date: 2026 (page version undated)
   - Source type: official docs
   - Confidence: medium
4. **Claim:** The only depth-on-land product tied to GloFAS is the global river flood hazard maps (Baugh et al. 2024): depth in metres, 7 return periods (10, 20, 50, 75, 100, 200, 500 yr), 90 m pixels, world excluding Greenland and Antarctica.
   - Source: https://developers.google.com/earth-engine/datasets/catalog/JRC_CEMS_GLOFAS_FloodHazard_v2_1
   - Quote: "The global river flood hazard maps are a gridded data set representing inundation along the river network." (resolution 90 m and RP10-RP500 depth bands per the same page)
   - Source date: dataset 2024-03-16 (EE catalog)
   - Source type: official docs (Earth Engine catalog of the JRC dataset)
   - Confidence: high
5. **Claim:** The hazard maps are produced by LISFLOOD-FP driven by LISFLOOD flows from the GloFAS v4.0 hydrological reanalysis, on MERIT-DEM / MERIT-Hydro, delivered as tiled GeoTIFFs (v2.1.2) in one folder per return period, with a tile-extent GeoJSON.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt
   - Quote: "This dataset incorporates the following other datasets: MERIT-DEM, MERIT-HYDRO, GloFAS v4.0 hydrological reanalysis"; "inundation simulations are performed with the hydrodynamic model LISFLOOD-FP."; "A GeoJSON file (tile_extents.geojson) is provided in the main directory"
   - Source date: README updated 2026-01-12
   - Source type: official docs
   - Confidence: high

### B. GloFAS: versions
6. **Claim:** GloFAS v4.0 went into production on 2023-07-26 (test release 2023-07-05); resolution moved from 0.1 deg (~10 km) to 0.05 deg (~5 km); new calibration at 1995 gauges with regionalisation for ungauged catchments; new return-period thresholds (1980-2022 climatology).
   - Source: https://confluence.ecmwf.int/x/Wx4oFw (ECMWF Confluence, GloFAS v4.0 page)
   - Quote: "GloFAS v4.0 has 0.05 degrees resolution (~5km)"; "fully operational GloFAS from 26 July 2023"; "1995 in-situ gauging stations"
   - Source date: 2023
   - Source type: official docs
   - Confidence: high (the page itself shows an internal conflict on the reference climatology start, 1979 vs 1980; irrelevant to us)
7. **Claim:** Later 4.x releases (4.1 2024-02-28, 4.3 2025-06-04, 4.5 2025-04-16 as listed) are minor; 4.5 is described as having "no impact on the GloFAS modelling results".
   - Source: https://confluence.ecmwf.int/spaces/CEMS/pages/265028624/GloFAS+versioning+system and https://confluence.ecmwf.int/x/p8ETJg
   - Quote: "This upgrade of GloFAS has no impact on the GloFAS modelling results." (v4.5 page); versioning table lists 4.1 = 2024-02-28, 4.3 = 2025-06-04, 4.5 = 2025-04-16
   - Source date: 2026-04-08 (v4.5 page version); versioning page undated. The table has an unexplained date order (4.5 before 4.3).
   - Source type: official docs
   - Confidence: medium
8. **Claim:** GloFAS v5.0 exists and, per the EWDS dataset page, is the operational version released 2026-07-15. It keeps 0.05 deg resolution, uses OS LISFLOOD v5.0.0, and is calibrated at 5,379 gauges (v4.0: 1,995). Reanalysis 1980-2025 (EWDS lists data from 1 January 1979 / 1980; sources differ on the start year). The Confluence pages still carried "2026-XX-XX" placeholders and the versioning page has no v5 row, so the operational switch date rests on the EWDS page alone.
   - Source: https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview ; https://confluence.ecmwf.int/x/FjolKQ
   - Quote: "Operational version - GloFAS v5.0 released 2026-07-15." (EWDS); "OS LISFLOOD v5.0.0" and "at 5379 in-situ gauging stations" (Confluence, v31 of the page); "0.05 x 0.05°"
   - Source date: 2026-11-11 (EWDS); 2026 (Confluence)
   - Source type: official docs
   - Confidence: medium (single source for operational date; CEMS news item could not be read)
9. **Claim:** The v5 change list includes a calibration that includes the streamflow (transmission) loss parameter and uses all stations with >=500 km2 drainage area and >=4 years of data, with no split sampling.
   - Source: web-search summary of the CEMS wiki calibration pages; the page was not opened by me. Treat as low confidence.
   - Quote: not obtained verbatim (not found)
   - Source date: 2026
   - Source type: official docs (not opened)
   - Confidence: low
10. **Claim:** Important for us: the JRC global hazard maps v2.1 are built on the v4.0 reanalysis, not v5. A v5-based hazard-map release was not found.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt
   - Quote: "GloFAS v4.0 hydrological reanalysis"
   - Source date: 2026-01-12
   - Source type: official docs
   - Confidence: high

### C. GloFAS: resolution, coverage, size limits
11. **Claim:** A GloFAS discharge cell is ~5 km (0.05 deg), i.e. ~2,500 ha, about 2,500 times a 1 ha plot; it describes a river reach, not a plot. The hazard maps are 90 m (~0.8 ha per pixel), so a 1 ha plot is about one pixel, but the depths are a river-network simulation, not local.
   - Source: https://confluence.ecmwf.int/x/Wx4oFw ; https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt
   - Quote: "GloFAS v4.0 has 0.05 degrees resolution (~5km)"; "3 arc seconds (~90 m)"
   - Source date: 2023; 2026
   - Source type: official docs
   - Confidence: high (areas are my arithmetic)
12. **Claim:** Minimum catchment size: in v4, only cells draining >500 km2 can become dynamic reporting points; flood summary layers show cells >250 km2; fixed points from v4.3 need >250 km2. Smaller tributaries and flash floods are not what GloFAS represents. (From a search summary of the CEMS wiki; pages not opened by me.)
   - Source: https://confluence.ecmwf.int/spaces/CEMS/pages/265028905/GloFAS+Reporting+Points (not opened; reported via search summary)
   - Quote: "Cells with smaller drainage area can not become reporting points." (as reported by the search tool, not verified)
   - Source date: 2025-2026
   - Source type: official docs (not opened)
   - Confidence: low
13. **Claim:** Peer-reviewed validation of the GloFAS-ERA5 reanalysis (v2.1, 0.1 deg): skilful in 86% of catchments; central Europe among the best regions; skill lowest in catchments <10,000 km2; dams and simplified reservoir rules cause discrepancies. No separate v4/v5 skill paper was found.
   - Source: https://essd.copernicus.org/articles/12/2043/2020/
   - Quote: "skilful in 86 % of catchments"; skill lowest "for catchments in the three categories <10 000 km2."; "simplified reservoir operating parameters were used based on expert opinion"
   - Source date: 2020
   - Source type: peer-reviewed
   - Confidence: high (for v2.1, not v4/v5)
14. **Claim:** GloFAS forecast paper: output grid ~11 km (v3), "catchments with higher hydrological flashiness have lower skill"; the authors say a 1 km "hyperresolution" model would be needed for local-scale prediction. No mention of flood defences.
   - Source: https://hess.copernicus.org/articles/27/1/2023/
   - Quote: "catchments with higher hydrological flashiness have lower skill"
   - Source date: 2023
   - Source type: peer-reviewed
   - Confidence: high
15. **Claim:** Hazard-map artefacts: very high depths in small channels; tile boundary effects; users told to be cautious. Flood defences are not mentioned in the README. Validation text: not found in the README.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt and the Earth Engine page above
   - Quote: "These artefacts are known and users should exercise caution when interpreting depth values"; "Very high water depths may result from limitations in the hydraulic modelling approach"
   - Source date: 2026-01-12
   - Source type: official docs
   - Confidence: high
16. **Claim:** The README states the spurious-depth layer covers small channels under 3,000 km2 for the 10-year return period (plus 2 km buffer). The Earth Engine page excludes only small islands with basins under 500 km2.
   - Source: README above; EE page above
   - Quote: "small channels (<3,000km^2)" (README, as returned by the tool); "depths greater than 10m are predicted in small channels" (EE band description)
   - Source date: 2026 / 2024
   - Source type: official docs
   - Confidence: medium

### D. GloFAS: access and licence
17. **Claim:** Discharge (forecast, reanalysis) is obtained from the CEMS Early Warning Data Store (EWDS) via its API/web form; an account and acceptance of the CEMS-FLOODS licence are needed (account step: not verified by me, standard for the CDS-style stores). File formats: GRIB2/NetCDF (not verified; not found in sources I opened).
   - Source: https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview
   - Quote: "CEMS-FLOODS datasets licence"
   - Source date: 2026-11-11
   - Source type: official docs
   - Confidence: low (licence name verified; account/format not found)
18. **Claim:** CEMS terms: attribution "Generated using Copernicus Emergency Management Service information [Year]" for distributed data and "Contains modified Copernicus Emergency Management Service information [Year]" for adapted data; free access for reproduction, distribution, public communication and adaptation; the terms do not mention commercial use; data is "information purposes only", not an official warning. The full CEMS-FLOODS licence text could not be opened (HTTP 500 / compressed PDF): not found.
   - Source: https://ewds.climate.copernicus.eu/licences/terms-of-use-cems
   - Quote: "Contains modified Copernicus Emergency Management Service information [Year]" (notices to be used "or similar")
   - Source date: rev. 11, undated
   - Source type: official docs
   - Confidence: medium
19. **Claim:** The JRC global hazard maps are distributed from the JRC open-data server (tif tiles, no login) and the README gives the licence as the Open Data Commons Open Database License v1.0 (ODbL); Earth Engine says the JRC datasets are "available without restriction on use or distribution". These two statements differ in tone. ODbL carries attribution and share-alike duties for derived databases (my knowledge, not from a source here): a team lawyer/lead should check whether a clipped COG counts as a derived database.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt ; EE page
   - Quote: "License information, restrictions on use: Open Data Commons Open Database License v1.0"; "The JRC datasets are available without restriction on use or distribution."
   - Source date: 2026-01-12; 2024
   - Source type: official docs
   - Confidence: high for the licence name; low for its consequences
20. **Claim:** Earth Engine hosts the hazard maps (JRC/CEMS_GLOFAS/FloodHazard/v2_1), so clipping needs no bulk download, but EE use is subject to our non-commercial free tier (see constraints). The JRC server alternative is a direct tile download. File sizes: not found.
   - Source: https://developers.google.com/earth-engine/datasets/catalog/JRC_CEMS_GLOFAS_FloodHazard_v2_1
   - Quote: "The extent comprises the entire world with the exception of Greenland and Antarctica."
   - Source date: 2024
   - Source type: official docs
   - Confidence: medium

### E. Google: products
21. **Claim:** Google's Flood Forecasting API is a forecast product (river gauge forecasts and flood status; also flash-flood search, significant events and serialized polygons). Its resources: flashFloods, floodStatus, gaugeModels, gauges, serializedPolygons, significantEvents.
   - Source: https://developers.google.com/flood-forecasting (overview) and https://developers.google.com/flood-forecasting/rest
   - Quote: "provides an interface to access real time riverine flood forecasts" (overview); `GET /v1/gauges:queryGaugeForecasts` "queries gauge forecasts." (REST list)
   - Source date: undated (current page)
   - Source type: official docs
   - Confidence: high
22. **Claim:** Access needs an API key, enabling the API, and a waitlist/approval; licence of API data is CC BY 4.0, but use is "primarily limited to non-commercial use".
   - Source: https://developers.google.com/flood-forecasting ; https://sites.research.google/gr/floodforecasting/resources/
   - Quote: "Accessing the Flood Forecasting API requires an API key and enabling the Flood Forecasting API."; "Once approved, we'll send you an email."; "Currently, the use of the flood forecasting API is primarily limited to non-commercial use."; "The data exposed by this API is under the CC BY 4.0 license and offered at no charge."
   - Source date: undated (current pages)
   - Source type: official docs
   - Confidence: high
23. **Claim:** Google publishes two historical datasets: Inundation History (how often each 128 m pixel was wet, 1999-2020, from satellite imagery, CC-BY-4.0, on Google Cloud Storage `flood-forecasting/inundation_history`) and GRRR (river discharge 1980-2023, via a Colab notebook; licence not stated). The Inundation History data is observed water occurrence, i.e. an observed-history product, not a modelled hazard.
   - Source: https://sites.research.google/gr/floodforecasting/resources/
   - Quote: "Explore historical data on how often each 128-meter pixel in the world has been wet between 1999 and 2020"; "The dataset is available under a CC-BY-4.0 license."; "Access global river discharge estimates from 1980 to 2023."
   - Source date: undated
   - Source type: official docs
   - Confidence: medium (format not stated; fetched through a summariser)
24. **Claim:** Flood Hub inundation maps are forecast-time maps for gauged rivers; a newer "inundation history" layer is for expert users and shows flood risk areas regardless of a current event. No return-period depth raster, API endpoint or country list for it was found; I found no evidence it is downloadable or covers Romania.
   - Source: https://blog.google/innovation-and-ai/products/advanced-flood-hub-features-for-aid-organizations-and-governments/
   - Quote: "Flood Hub expert users can view flood risk areas in high resolution over the map regardless of a current flood event."
   - Source date: 2025 (the blog; exact date not shown)
   - Source type: vendor
   - Confidence: medium (vendor-only)
25. **Claim:** Google's inundation model (HESS 2022): maps at 16 m resolution (evaluated at 64 m), threshold or "manifold" approach driven by gauge stage; designed for gauged rivers; best on large slow rivers; flash floods and basins <1,000 km2 listed as future work; no ground truth for depth; flood defences not discussed.
   - Source: https://hess.copernicus.org/articles/26/4013/2022/
   - Quote: "a 16 × 16 m2 spatial resolution"; "there are no ground truth data for flood inundation depth"; "aim to expand the technique to small-to-medium basins (< 1000 km2) and to handle flash floods."
   - Source date: 2022
   - Source type: peer-reviewed
   - Confidence: high (note: the study area is India/Bangladesh, and the 2022 method may have changed)
26. **Claim:** Google's global forecast model (Nature 2024): trained on 5,680 gauges, predicts discharge; reliability at up to 5 days similar to GloFAS nowcast; Europe was the highest-scoring continent for GloFAS (F1 = 0.32 for 5-yr events); GloFAS stations <500 km2 dropped for the comparison; the authors say the comparison "favours the GloFAS benchmark". Flash floods and urban floods are future work. The article is CC BY 4.0, trained model code is public but input data licences are not distributable.
   - Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10954541/ ; https://research.google/blog/using-ai-to-expand-global-access-to-reliable-flood-forecasts/
   - Quote: "the highest-scoring continent (Europe, F1 = 0.32)"; "favours the GloFAS benchmark"; "river reaches across over 80 countries" (blog)
   - Source date: 2024-03-20
   - Source type: peer-reviewed (Nature); vendor (blog)
   - Confidence: high for the paper, medium for the blog
27. **Claim:** Romania is on Google's Flood Hub country list ("more than 150 locations"); Romania was announced in May 2023 as part of expanding to 80 countries. Whether there are gauges / forecast points on the Danube at Galati, Siret or Prut, and whether inundation maps exist there: not found. Minimum river size represented by Google forecasts: not found (the paper's evaluation gauges span 2.1 km2 to 4.69 million km2, which is the evaluation sample, not a coverage guarantee).
   - Source: https://support.google.com/flood-hub/answer/16508958?hl=en ; https://www.euronews.ro/articole/flood-hub-prognoza-inundatiilor-cu-ajutorul-ai-de-la-google-extinsa-si-in-romania
   - Quote: "Our models are currently covering more than 150 locations." (help centre); euronews.ro (2023-05-23) said Romania "va fi extins și în România" per the tool summary (not a verified verbatim quote; confidence low for this part)
   - Source date: 2023-05-23 (euronews); help page undated
   - Source type: vendor; blog/news
   - Confidence: medium for "Romania is listed"; none for gauge/inundation coverage

## Relevance to LandHorizon
- **Google Flood Hub / Flood Forecasting API: dead end for a plot-level hazard layer.** It is a real-time forecast (gauge discharge/status), gated by waitlist and API key, and its stated use is "primarily limited to non-commercial use", which conflicts with a product. It cannot be precomputed once into a COG. Inundation maps are gauge-driven, tied to a forecast, and no downloadable return-period raster was found. Coverage at Galati (gauges, inundation) not found. Google's Inundation History dataset (128 m, CC-BY-4.0, 1999-2020) is a free, openly licensed, downloadable observed water-occurrence layer; it duplicates the Sentinel-1 role rather than adding a model, and its file format and ingest cost are not found. It could be a cheap cross-check or a roadmap item, nothing more.
- **GloFAS discharge (forecast, reanalysis, v4 or v5): not usable per plot.** Variable is discharge on a ~5 km grid, a river-reach quantity. It would not change the pipeline unless paired with a hydraulic model, which is out of scope. Min. catchment sizes (250-500 km2 for reporting points; lowest skill under 10,000 km2) mean the Sept 2024 Galati flood (small tributary / flash flooding) is outside what it represents. Could still be used regionally: v5 return-period thresholds for the Danube/Siret/Prut as context (not plot-level).
- **Best-fitting global modelled product: JRC/CEMS global river flood hazard maps v2.1.** Depth in metres, 7 return periods (RP10-RP500), 90 m GeoTIFF tiles, no login on the JRC server, also in Earth Engine. This is the only candidate that fits the pipeline (one precompute of a tile clip into a COG per return period; size for a Galati-sized AOI: not found but small, order of tens of MB at 90 m, my estimate, not sourced). Fit with the constraints:
  - Free and open: yes; ODbL (README) vs "without restriction" (EE). Needs attribution and a lead's decision on share-alike.
  - Resolution: ~90 m, so a 1 ha plot is about one pixel; present it as "river-network hazard in the surrounding ~90 m cell", not a plot depth.
  - Return periods come from the model, not our 10 years of Sentinel-1, which respects the "must not claim return periods from our own data" rule, provided it is shown as a separate modelled layer with its source named. It must be labelled screening, not official: small-channel artefacts (<3,000 km2 for RP10), unknown defences, no pluvial/flash flooding.
  - Built on GloFAS v4.0 (not v5); its Danube performance is not validated in the sources I read: not found. Independent check against our GFM/Sentinel-1 flood extent at the Sept 2024 event, split by event, is the obvious test, with the pass thresholds fixed beforehand.
  - Coverage of Galati, lower Danube, Siret, Prut: the extent is "the entire world with the exception of Greenland and Antarctica"; whether the tiles have artefacts around the Danube delta/confluence is not found (needs a look at the real tiles).
  - Cost/compute: no EE compute needed if read from the JRC server; roughly a day of one person's time to clip and COG it (my estimate). No new hazard sensor; it is a new layer, so under the plan's "new hazard" rule it needs lead approval.
- Evidence contract: a new modelled field would change the shape of `api/main.py`; needs lead review and must stay `unknown` where tiles have no data (do not default to 0 m).

## Open questions
- Full text of the CEMS-FLOODS licence (commercial use, derived data): the page returned HTTP 500 and the PDF was not readable. Needs a manual read.
- Does ODbL share-alike apply to a clipped, rasterised-and-quantised COG shown in a product? Needs a lead/legal call.
- Which GloFAS fixed reporting points exist on the Danube at Galati, the Siret and the Prut, and are the v5 operational forecasts live? Not found. The CEMS news site (React) could not be read.
- Did the JRC publish hazard maps from GloFAS v5, or only v2.1.2 (from v4.0)? Not found.
- Google Flood Hub gauge list for Romania: not found (would need the Flood Hub UI or API access).
- Skill of the hazard maps in the lower Danube: no validation found; the EFAS/European hazard-map and Romanian products are other researchers' scope.

## Review
Reviewed: 2026-11-12, by a reviewer who did not write this file.

Method: every cited URL was re-opened. Like the researcher, I read pages through a fetch tool that summarises, so each quote was checked by asking whether the exact string is on the page; I did not see raw HTML. Two sources could not be read (noted below). Nothing in the fetched pages or in this file tried to give me instructions.

Counts: 20 verified, 4 unsupported, 1 misquoted, 2 unreachable.

### Verdicts
1. `verified`: both quotes are on the EWDS page; variable is "River discharge in the last 24 hours", m3 s-1; update date 2026-11-11. "Listed as operational" is accurate as a description of the page, but see claim 8 before relying on it.
2. `unreachable`: the CEMS news page returns only "CEMS-Floods React". The same facts are covered by claims 1 and 6.
3. `verified`: "From 2003-03-27 to real time" and "new return period thresholds and snow water/soil moisture anomaly maps based on a climatology from 1980 – 2025." are on the page. The page I got is not an old placeholder: it is titled "Upcoming GloFAS release (v5)", last modified 22 Oct 2026, and gives the release date as "2026 (TBD)".
4. `verified`: the quote is the start of a longer sentence (the page has a comma, not a full stop, and goes on "for seven different flood return periods"). 90 m, seven RP depth bands in metres, the Baugh et al. 2024 citation and the 2024-03-16 date are all on the page. "The only depth-on-land product" is an absence claim I cannot prove; I found no other.
5. `verified`: all three quotes are in the README exactly; "Dataset version 2.1.2", "Last update of the README file: 12.01.2026". The README says seven return periods in "RP<XXX>/" folders but does not list their values; those come from the Earth Engine page.
6. `verified`: all three quotes are on the page (last modified 28 May 2025), plus "pre-release ... from 05 July 2023", the regionalisation sentence and "climatology from 1980 – 2022".
7. `unsupported`: the dates (4.1 = 2024-02-28, 4.3 = 2025-06-04, 4.5 = 2025-04-16) and the v4.5 "no impact" quote check out, but nothing quoted shows that 4.1 and 4.3 are minor. The table also has 4.2 (2024-11-12) and 4.4 (2025-09-10), which the claim leaves out, and the v4.5 page is an old placeholder version (v20) with its release date as "2025-xx-xx". No bearing on LandHorizon.
8. `unsupported`: the technical facts are verified (0.05 x 0.05°, "OS LISFLOOD v5.0.0", "5379 in-situ gauging stations", EWDS "1 January 1979 to near real time for v5.0, and v4.0", wiki "1980-01-01 to near present"). The EWDS quote is there, but it does not establish that the v5 forecast system is operational: the current wiki page, modified 22 Oct 2026, still says release "2026 (TBD)" and "with launch expected soon". The EWDS line most likely marks the release of the reanalysis dataset. Treat it as "v5.0 reanalysis released July 2026; operational forecast switch not confirmed".
9. `unsupported`: no URL and no quote were given. I opened three versions of the v5 wiki page (x/FjolKQ, x/bDolKQ, x/FzolKQ); none states a drainage-area threshold, years of data, split sampling or a transmission-loss parameter. They only link to a calibration page I did not find.
10. `verified`: the README lists "GloFAS v4.0 hydrological reanalysis" as an input. I also found no v5-based hazard map.
11. `verified`: both quotes are there. The areas are rounded: at Galați's latitude a 0.05° cell is about 5.6 x 3.9 km (about 2,200 ha) and a 3 arc-second pixel about 93 x 65 m (about 0.6 ha, not 0.8), so a 1 ha plot is one to two pixels. The conclusion does not change.
12. `unreachable`: the cited Reporting Points page returned empty content twice. The quoted sentence exists on a different page, "GloFAS v4 dynamic points" (https://confluence.ecmwf.int/x/Zc9PF, last updated 15 Sep 2023), in lower case inside a longer sentence, together with "only cells with an upstream drainage area greater than 500km2 are considered in the dynamic point algorithm" and "all cels with an upstream area greater than 250km2" for the summary layers. The ">250 km2 for fixed points from v4.3" part I could not open anywhere. Re-cite to x/Zc9PF and the first two thresholds would be verifiable.
13. `verified`: quotes present (the second is cut mid-sentence: "skill is lowest for catchments in the three categories <10 000 km2 with median KGESS ..."). The paper is GloFAS-ERA5 v2.1 at 0.1°, published 7 Sep 2020, and says "Performance is best in Brazil ..., central Europe, and the eastern and western regions of the United States." Note that "skilful" only means better than using the observed mean flow as the prediction, which is a low bar.
14. `unsupported`: the flashiness quote is exact, the "hyperresolution ... in the order 1 km" statement is there, and flood defences are not mentioned. But the paper (Harrigan et al., 2 Jan 2023) describes GloFAS v2.1, with v2.2 as a service-only upgrade, on a "0.1° (~11 km)" network, not v3 as the claim says. With "(v3)" changed to "(v2.1)" the claim would be verified.
15. `verified`: both quotes are in the README exactly; the tile sentence reads "water depths may also be unrealistic due to boundary effects between individual tiles or due to residual DEM issues". The README does not mention flood defences or validation.
16. `verified`: the README has "small channels (<3,000km^2) for the 10-year return period, plus a 2km buffer"; the Earth Engine page has "where depths greater than 10m are predicted in small channels" and "small islands with river basins smaller than 500 km²".
17. `verified`: "CEMS-FLOODS datasets licence" is on the page. The claim says the file format was not found, but the same page states "GRIB2 and NetCDF-4". The account step is still unchecked.
18. `verified`: both notices, "or similar", "information purposes only" and the list of permitted uses are on the page; the word "commercial" does not appear. The page is dated: "Last modified: 07/06/2023". I could open the CEMS-FLOODS licence itself; see "Missed" below.
19. `verified`: both quotes are present on their pages. The README names the licence only; it says nothing about share-alike or commercial use. The share-alike reading is the researcher's own knowledge, as they say, and no source in this file backs it.
20. `verified`: the quote is cut short. The page's sentence continues "and small islands with river basins smaller than 500 km²" (the researcher notes this in claim 16). Dataset ID confirmed. File sizes: I did not find them either.
21. `misquoted`: the second quote was altered. The REST page says "Query gauge forecasts.", not "queries gauge forecasts.". The first quote is exact and the six resources (flashFloods, floodStatus, gaugeModels, gauges, serializedPolygons, significantEvents) are all listed, so the facts stand; only the quote needs fixing.
22. `verified`: the API-key, "Once approved" and CC BY 4.0 quotes are on the developers page, which also has a waitlist form; the "primarily limited to non-commercial use" quote is on the resources page.
23. `verified`: all three quotes are on the resources page, which adds "derived from satellite imagery" without naming the satellite and links the Cloud Storage path `flood-forecasting/inundation_history`. No licence is stated for GRRR. "Observed, not modelled" is a fair reading.
24. `verified`: the quote is the second half of a sentence that starts "With the inundation history maps,". The post is dated 18 Feb 2025. It describes no download, no country list and no definition of "expert users". Vendor source only.
25. `verified`: the three quotes are present (the last continues "which appear only a few hours following an intense storm"); "evaluated at a 64 × 64 m2 spatial resolution"; study area India and Bangladesh, 2021 monsoon; no mention of defences, levees or embankments. I did not check "best on large slow rivers" against a quote.
26. `verified`: both paper quotes are exact; 5,680 gauges; the F1 = 0.32 is the GloFAS nowcast score for 5-year events; "we lack the distribution license for the input data products". Two details: the paper says "all GRDC stations with a drainage area smaller than 500 km2 were discarded" (GRDC stations in the GloFAS benchmark), and the words "flash" and "urban" are not in the paper at all. "flash floods and urban floods" as future work is from the Google blog (20 Mar 2024), which is vendor text.
27. `verified`: the help-centre quote is exact and Romania is on the list; the euronews.ro article (23/05/2023) contains "va fi extins și în România" and "în 80 de țări". The help page does not separate countries with inundation maps from countries with gauge forecasts only.

### What the researcher missed
- **GloFAS v5 is probably not operational yet for forecasts.** The current wiki page (22 Oct 2026) says "2026 (TBD)" and "launch expected soon": https://confluence.ecmwf.int/x/38QHIQ. The versioning page (16 Apr 2026) has no v5 row and calls 4.5 the "Latest operational GloFAS release". A CEMS news item of 16 Jul 2026 reportedly announces only the v5.0 reanalysis, with forecasts to run pre-operationally alongside the current version first; I could not open it (React page), so that part rests on a search snippet: https://global-flood.emergency.copernicus.eu/news/252-the-new-copernicus-glofas-v50-hydrological-reanalysis-has-been-released/
- **The CEMS-FLOODS licence can be opened** (first open question): https://ewds.climate.copernicus.eu/licences/cems-floods (rev. 1, undated). Free access for (a) reproduction, (b) distribution, (c) communication to the public, (d) adaptation, modification and combination, (e) any combination; the word "commercial" does not appear, so it is neither allowed nor forbidden in words; the two attribution notices are required; "Access to this restricted data will be granted only to specific users and upon registration" for some data; the data "does not constitute in any way a flood warning".
- **The hazard maps have no published description or validation.** The README gives the reference as "An updated dataset of global and European flood hazard maps. Manuscript under preparation." with DOI and PID "NA". Version 2.1 is therefore a producer's dataset with no peer-reviewed or independent validation that I could find: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt
- **The README does not say what an empty pixel means.** It gives no NoData value, no minimum upstream area for modelled rivers, and does not say whether a pixel without depth is "modelled dry" or "river not modelled" (same URL). This matters for the `unknown` rule, see below.
- **Flood defences and discharge error, from an independent 2026 paper.** Sadana et al., HESS 30, 5491 (1 Sep 2026), validate a different inundation model (SFINCS) forced with the same GloFAS/LISFLOOD v4.0 discharge on 499 events: global topography "is too coarse to include river flood defences"; "mean CSI of 0.39 using GloFAS modelled discharges", against 0.67 for ten US events forced with observed discharge. It does not test the JRC maps, so it is indirect evidence that undefended, GloFAS-driven maps should be expected to be rough: https://hess.copernicus.org/articles/30/5491/2026/
- **GloFAS v4 skill evidence exists, though not as a paper.** The CEMS wiki reports the share of stations with KGE' > 0.7 rising "from 38% (GloFAS v3) to 58% (GloFAS v4)" and that "The lowest performances ... are often concentrated in catchments with strongly regulated rivers": https://confluence.ecmwf.int/spaces/CEMS/pages/340755428/GloFAS+v4+calibration+hydrological+model+performance. A 2026 preprint comparing v2.1 and v4.0 also turned up in search; I did not open it: https://egusphere.copernicus.org/preprints/2026/egusphere-2026-3321/egusphere-2026-3321.pdf
- **A third licence statement for the hazard maps is unchecked.** The JRC Data Catalogue entry returned "Request Rejected" for me: https://data.jrc.ec.europa.eu/dataset/jrc-floods-floodmapgl_rp50y-tif. Someone should read it by hand before choosing between "ODbL" and "without restriction".
- **Google's resources page also lists the Groundsource Flash Flood Dataset**, "an open global dataset of 2.6 million historical flood events derived from news articles". It is not a hazard layer, but it is a possible independent reference for flash-flood events: https://sites.research.google/gr/floodforecasting/resources/
- **Flood Hub has public per-gauge pages**, including ones labelled "Danube River" (seen in search results, not opened, location within Romania not confirmed), so the open question on Romanian gauges can probably be answered in the Flood Hub UI: https://sites.research.google/gr/floodforecasting/flood-hub-expert-mode

### Problems in "Relevance to LandHorizon"
- **The proposed validation test contradicts the file's own reasoning.** The GloFAS bullet says the Sept 2024 Galați flood was "small tributary / flash flooding" and outside what GloFAS represents; the hazard-map bullet then calls a check against that same event "the obvious test". If the event was on small streams, a river-network map driven by GloFAS v4.0 is expected to miss it, and a miss tells us nothing about the Danube, Siret or Prut. Also, no claim in this file describes the Sept 2024 flood, so that characterisation is unbacked here. A single event extent against a return-period map also needs a stated choice of return period before precision and recall mean anything (constraints: thresholds written before the test).
- **"Stay `unknown` where tiles have no data" is not enough.** Because the README does not define empty pixels or the smallest modelled river, a plot with no depth could be modelled dry, on an unmodelled small stream, or exposed only to pluvial flooding. Showing that as 0 m or "no hazard" would break the "missing data is `unknown`" rule; the file does not say how the two cases would be told apart.
- **Return periods in the product.** The file argues that RP layers respect the rule because they are not from our Sentinel-1 data. The constraint also says the product is "a screening indicator ..., not a probability". Showing 1-in-100-year depths puts probability language in front of users, from a map with no published validation, known small-channel artefacts and no flood defences. That is a decision for the lead, not something the verified claims settle.
- **"Free and open: yes" is premature.** The README says ODbL, Earth Engine says "without restriction", the JRC catalogue entry is unread, and the share-alike consequences are unsourced. Product use is unresolved, not confirmed. The Earth Engine route also falls under the non-commercial free tier (the researcher does flag this in claim 20).
- **"Needs lead approval" under the "new hazard" rule is not what the constraints say.** They rate a new hazard or sensor as out of scope after the 22 Nov gate, and require lead review for an evidence-contract change. A new modelled layer changes the contract and adds a data source; with the gate on 22 Nov, flood validation due 29 Nov and the GFM spring false-positive problem still open, this is realistically a roadmap item. The file does not say that this layer does nothing for the open GFM decision.
- **Unsourced estimates.** "Tens of MB" and "roughly a day of one person's time" are the researcher's guesses (labelled as such); file sizes were not found by either of us. The explainability constraint is not addressed: the team would have to explain a LISFLOOD reanalysis, extreme-value return periods and LISFLOOD-FP on MERIT with no paper to point to.
- **GloFAS thresholds "as context".** The suggestion to use v5 return-period thresholds for the Danube, Siret and Prut rests on claim 8 (v5 status not confirmed) and claim 12 (not verified). The licence does not forbid it, but the data is discharge at about 5 km and must be presented as regional, as the file says.
- **Google bullets hold up.** "Dead end for a plot-level hazard layer" is backed by verified claims 22, 23, 24 and 27 (claim 21's facts are right, its quote needs fixing). The Inundation History dataset ends in 2020, so it cannot be checked against 2024 events, and its sensor is not named, so it cannot yet be called an independent-sensor reference.
