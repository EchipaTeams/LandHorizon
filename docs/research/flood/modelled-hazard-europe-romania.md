# Which European or Romanian modelled flood-hazard products could serve as a hazard layer for plot-level screening in Galati, and on what terms?
Date: 2026-11-11
Scope: EFAS, the JRC European river flood hazard maps, Romanian Floods Directive maps (RO-FLOODS / inundatii.ro / ANAR), and what Imoreview shows. Out of bounds: GloFAS and the global JRC maps, running our own hydrodynamic model, ML, Sentinel-1/GFM observed mapping.

Method note: pages were read through a fetch tool that returns a summary with quoted passages. Quotes below are those passages as returned; the few PDFs that could not be decoded (RO-FLOODS brochures, EFAS Condition of Access, Law 179/2022 docx, EUR-Lex HVD regulation) are NOT cited. The JRC Data Catalogue pages (data.jrc.ec.europa.eu) returned "Request Rejected" to the fetch tool, so JRC claims rest on the JRC file server (README, CHANGELOG, directory listing) and the ESSD paper. Nothing was downloaded, so no raster was inspected.

## Claims

### A. JRC / CEMS European river flood hazard maps
1. **Claim:** The current release is v3.1.1 (5 Mar 2026), with depth maps for nine return periods (RP10, 20, 30, 40, 50, 75, 100, 200, 500), at 3 arc seconds (~90 m), as GeoTIFF, plus permanent-water-body and "spurious depth" layers. Each depth file is roughly 260-334 MB (European extent, single files, not tiles).
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/CEMS-EFAS/flood_hazard/README.txt
   - Quote: "3 arc seconds (~90 m)" and "Dataset version 3.1.1" and "nine different flood return periods"
   - Source date: 2026-03-05 (README last update)
   - Source type: official docs
   - Confidence: medium (README text; file names/sizes from the directory listing at https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/, which lists Europe_RP10_filled_depth.tif ... Europe_RP500_filled_depth.tif)
2. **Claim:** Version history: v1.0.0 (2014), v2.0.0 (Apr 2022, the ESSD-described 100 m dataset), v3.0.0 (Mar 2024), v3.1.0 (Nov 2024), v3.1.1 (Mar 2026, fixes depth artefacts from modelling and DEM issues). The v3 dataset description paper is "Manuscript under preparation" (not peer-reviewed publication found).
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/CHANGELOG.txt
   - Quote: "Correction of artefacts identified in some areas of the flood depth maps resulting from modelling and DEM-related issues."
   - Source date: 2026-03-05
   - Source type: official docs
   - Confidence: high for versions; the "manuscript under preparation" point is from the README (quote: "An updated dataset of global and European flood hazard maps. Manuscript under preparation.")
3. **Claim:** v3.1.0 added a layer flagging small channels (under 3,000 km2 catchment) where the 10-year depth exceeds 10 m, i.e. the provider itself marks small-channel results as unreliable.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/CHANGELOG.txt
   - Quote: "Europe_spurious_depth_areas.tif" (file name quoted; the "under 3,000 km2" and "10 m" details are in the changelog entry as returned by the fetch tool, not reproduced verbatim)
   - Source date: 2024-11-08
   - Source type: official docs
   - Confidence: medium
4. **Claim:** For the v2 (2022) dataset the minimum modelled river is 500 km2 upstream area, defences are NOT represented, and the authors list those as main limitations. The v3 README states neither minimum catchment nor defences: **not found for v3**.
   - Source: https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
   - Quote: "rivers with upstream drainage areas larger than 500 km2" and "the flood maps developed do not account for the influence of local flood defences, in particular dyke systems" and "the absence of flood protections and rivers with an upstream area below 500 km2"
   - Source date: 2022-04-07
   - Source type: peer-reviewed
   - Confidence: high for v2; low as a statement about v3
5. **Claim:** Published validation (v2) against official maps of Hungary, Italy, Norway, Spain, UK: on average two-thirds of reference extent is identified; CSI approaches 0.5 only at long return periods; high false alarms in Hungary and Norway; England underestimates. Romania was not among the validation countries.
   - Source: https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
   - Quote: "the modelled maps can identify on average two-thirds of reference flood extent"
   - Source date: 2022-04-07
   - Source type: peer-reviewed
   - Confidence: medium (per-country table was an image and not read; country list from a search summary of the paper, https://essd.copernicus.org/articles/14/1549/2022/)
6. **Claim:** Licence: the README names the Open Data Commons Open Database License v1.0, while the folder's copyright.txt says the dataset is CC BY 4.0 with reuse allowed given credit and changes indicated. The two files disagree; both permit commercial reuse with attribution, but ODbL adds share-alike for derived databases, which matters if we redistribute a derived raster.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/CEMS-EFAS/flood_hazard/README.txt ; https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/copyright.txt
   - Quote: "Open Data Commons Open Database License v1.0" (README); copyright.txt: "Reuse is allowed provided appropriate credit is given and any changes are indicated." (as returned by the fetch tool, which said it could not reproduce the file verbatim, so treat that second quote as medium)
   - Source date: 2026-03-05 (README); copyright.txt shows "(c) European Union, 1995-2026"
   - Source type: official docs
   - Confidence: medium
7. **Claim:** README domain line for v3 reads "European extended domain (-24.54, 67.26; 27.81, 71.13)". Taken literally this would stop at about 27.8 E, west of Galati (about 28.0 E). The axis order is unclear, so whether Galati is inside the raster is **not confirmed**.
   - Source: https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/CEMS-EFAS/flood_hazard/README.txt
   - Quote: "European extended domain (-24.54, 67.26; 27.81, 71.13)"
   - Source date: 2026-03-05
   - Source type: official docs
   - Confidence: low (ambiguous; must be checked by reading the GeoTIFF header, e.g. with a ranged read of the COG/TIF)
8. **Claim:** The v2 paper says the maps are a component of EFAS, built with LISFLOOD discharge (5 km, daily) and LISFLOOD-FP inundation at 100 m; so the EFAS-linked inundation product is this JRC dataset, not something in the EFAS discharge archive.
   - Source: https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
   - Quote: "The hydrological input is at 5 km and daily resolution." (as returned; the "component of EFAS" wording is from a search summary of the same paper)
   - Source date: 2022-04-07
   - Source type: peer-reviewed
   - Confidence: medium

### B. EFAS
9. **Claim:** All real-time EFAS forecasts are restricted to EFAS partners; they are released publicly after a 30-day embargo. Historical and other non-real-time data are public.
   - Source: https://confluence.ecmwf.int/x/EYaBEQ
   - Quote: "All real-time EFAS forecasts and products are restricted and only accessible to \"EFAS partners\"" ... "after an embargo of 30 days."
   - Source date: not shown (undated wiki)
   - Source type: official docs
   - Confidence: high
10. **Claim:** The EWDS forecast dataset is available "with a 30-day delay", resolution 1 arcmin (v5) vs 5 km (v4), licence listed as "CEMS-FLOODS datasets licence" (terms not read).
    - Source: https://ewds.climate.copernicus.eu/datasets/efas-forecast
    - Quote: "1x1 arcminute for version 5.0, 5x5km for version 4.0 and older." and "The real-time data is only available to EFAS partners."
    - Source date: not shown
    - Source type: official docs
    - Confidence: high for resolution/restriction; licence text not found
11. **Claim:** EFAS produces discharge, not inundation: the LISFLOOD OS setup is ~1.5 km (1 arcmin); thresholds are return-period discharges at river points, downloadable as maps from the Auxiliary Data page.
    - Source: https://confluence.ecmwf.int/spaces/CEMS/pages/293701841/7+FAQ+in+EFAS
    - Quote: "OS LISFLOOD model set-up has 1 arcmin resolution (approximately 1.5 km)" and "is used to calculate return period thresholds for every point along the river network."
    - Source date: not shown
    - Source type: official docs
    - Confidence: high
12. **Claim:** EFAS historical simulation dataset (1992 to near real time) and reforecasts are open via EWDS with a free account. Only found through a search-result summary; the EWDS historical page itself failed to load ("socket hang up").
    - Source: https://ewds.climate.copernicus.eu/datasets/efas-historical
    - Quote: not found (page not opened)
    - Source date: not found
    - Source type: official docs
    - Confidence: low

### C. Romanian Floods Directive maps (RO-FLOODS, inundatii.ro, ANAR)
13. **Claim:** RO-FLOODS updated hazard and risk maps for all 526 Areas of Potential Significant Flood Risk (APSFR), with World Bank support; hazard maps give extent, depth, in some cases velocity, for several annual exceedance probabilities plus a climate-change scenario; LiDAR-derived DTMs were used.
    - Source: https://www.worldbank.org/en/results/2023/03/22/flood-hazard-and-risk-maps-development-and-use-of-flood-maps-to-strengthen-integrated-flood-risk-management-in-romania
    - Quote: "New flood hazard maps indicating flood extent, flood depth and in some cases flood velocities" ; "the use of airborne Light and Detection Ranging (LIDAR) sensors for developing new digital terrain models"
    - Source date: 2023-03 (from URL)
    - Source type: official docs (World Bank, provider-side)
    - Confidence: medium
14. **Claim:** Maps were released 7 Nov 2022 on www.inundatii.ro, "accessible to anyone", via a web GIS viewer; the ministry article mentions no download and no resolution. The Ministry (MMAP), ANAR and INHGA with the World Bank ran the project; endorsed by 11 basin committees and reported to the EC in Sept 2022.
    - Source: https://www.bursa.ro/ministerul-mediului-hartile-de-hazard-si-risc-la-inundatii-hhri-actualizate-sunt-accesibile-publicului-46491842
    - Quote: "disponibile pe www.inundatii.ro" (available on www.inundatii.ro) ; "accesibilă oricărei persoane interesate" (accessible to any interested person)
    - Source date: 2022-11-07
    - Source type: blog (news reprint of a ministry statement)
    - Confidence: medium
15. **Claim:** The exact scenarios (10 %, 1 %, 0.1 %) are stated only by Imoreview, not by an official page I could read. Official wording is only "different annual exceedance probabilities" (claim 13). Official statement of the three scenarios: **not found** (brochures and presentation PDFs could not be decoded).
    - Source: https://imoreview.ro/inundatii
    - Quote: "Scenariile consultate corespund unor probabilități anuale diferite: aproximativ 10%, 1% și 0,1%." (The scenarios consulted correspond to different annual probabilities: about 10%, 1% and 0.1%.)
    - Source date: not shown (page cites 2026 data elsewhere)
    - Source type: vendor (competitor)
    - Confidence: low-medium (secondary, single source)
16. **Claim:** Flash and pluvial floods: sources conflict. The World Bank page says modelling covered "fluvial flooding, flash floods, pluvial and coastal flooding". ANAR (2014, about the older cycle) says the maps show "numai din revărsarea de râuri" (only river overflow) and that flash-floods are not covered. Imoreview states pluvial flooding can occur "și în afara zonelor modelate de revărsare" (also outside the modelled overflow zones). Whether the published inundatii.ro polygons include pluvial/flash scenarios in Galati: **not found**.
    - Source: https://www.mediafax.ro/social/anar-hartile-de-hazard-si-de-risc-vor-fi-folosite-pentru-planificare-interventiile-in-functie-de-avertizari-12519624/amp
    - Quote: "hărţile de hazard prezintă zonele inundabile numai din revărsarea de râuri" (hazard maps show flood-prone areas only from river overflow)
    - Source date: 2014-04-24 (updated 2020-03-31)
    - Source type: blog (news quoting ANAR)
    - Confidence: medium (old; superseded cycle)
17. **Claim:** Access routes. (a) inundatii.ro web viewer. (b) ANAR publishes an INSPIRE WMS "NZ.ZoneInundabile" (RO.ANAR) with GetCapabilities on portal-gis.rowater.ro. (c) The EEA CIS2 registry lists two datasets (Inundatii.RO "Flood Hazard and Risk Maps" and ANAR flood-zone GIS layers) with Data Policy "Freely accessible" and dissemination "View and Download Service", format "Multiple", no licence field and no URL. I could not open the WMS (404 on my guessed URL), could not open the INSPIRE geoportal record, and found no confirmed bulk download, ArcGIS REST endpoint, or published licence.
    - Source: https://cis2.eea.europa.eu/data/915
    - Quote: "View and Download Service" ; "Freely accessible"
    - Source date: not shown
    - Source type: official docs (EEA registry)
    - Confidence: medium for the registry entry; the WMS name comes from a search summary only (low)
18. **Claim:** Copernicus In Situ use case confirms the Inundatii.RO data contain extent, depth and velocity, and that ANAR flood-zone datasets exist as separate "Flood Zones Datasets"; it states no access conditions or licence.
    - Source: https://insitu.copernicus.eu/resources/use-cases-folder/use-of-cems-aerial-component-and-romanian-national-data-for-flood-risk-assessment
    - Quote: "Flood Hazard and Risk Maps (flood extent, depth and velocity maps) provided by Inundatii.RO"
    - Source date: not shown
    - Source type: official docs
    - Confidence: medium
19. **Claim:** Reuse right in law: Romania transposed the Open Data Directive (EU) 2019/1024 in Law no. 179/2022 (title: "privind datele deschise şi reutilizarea informaţiilor din sectorul public"). Whether flood hazard maps are high-value datasets or carry a specific licence: **not found** (the law text and Regulation (EU) 2023/138 could not be read by my tools). The INSPIRE directive gives view/discovery access rights, not by itself a reuse licence: not verified from a source.
    - Source: https://www.onrc.ro/documente/legislatie/LEGE nr. 179 din 9 iunie 2022.docx
    - Quote: "privind datele deschise şi reutilizarea informaţiilor din sectorul public" (title as returned by the search tool)
    - Source date: 2022-06-09
    - Source type: official docs (law title only)
    - Confidence: low (title only)
20. **Claim:** A follow-on project "RO-FLOODS III" (Cycle III hazard and risk maps plus a national hazard map) is tendered in 2026; the Cycle III maps do not exist yet. Only from a search summary of a TED notice (https://ted.europa.eu/it/notice/420756-2026/pdf), not opened.
    - Source: https://ted.europa.eu/it/notice/420756-2026/pdf
    - Quote: not found (page not opened)
    - Source date: 2026
    - Source type: official docs
    - Confidence: low

### D. Imoreview
21. **Claim:** Imoreview shows "Zone inundabile: Hărțile oficiale de hazard, pe adresă" (official hazard maps, by address), free without an account. Its /inundatii guide names RO-FLOODS (inundatii.ro) as the source, compares an address *point* with the maps, reports scenario and estimated depth where intersected, and says a point check "nu descrie fiecare colț al parcelei" (does not describe every corner of the plot). It does not claim a data licence on the pages read; Terms page not read.
    - Source: https://imoreview.ro/inundatii
    - Quote: "Poziția adresei este comparată cu hărțile oficiale RO-FLOODS." (The address position is compared with the official RO-FLOODS maps.)
    - Source date: not shown (site shows August 2026 market data)
    - Source type: vendor (competitor)
    - Confidence: high for what Imoreview says; says nothing about licence

### E. Other candidates
22. **Claim:** ICPDR Danube FloodRisk maps are PDF maps for catchments larger than 4,000 km2; Romania/Bulgaria risk data only for the Danube itself; no GIS download found. Not suitable for plots. (Search summary only; ICPDR page returned 403 to fetch.)
    - Source: https://icpdr.org/tasks-topics/tasks/flood-risk-management/flood-hazard-and-risk-maps
    - Quote: not found (page not opened)
    - Source date: not found
    - Source type: official docs
    - Confidence: low
23. **Claim:** The Sept 2024 Galati/Vaslui event is documented by CEMS Rapid Mapping (EMSR758): "major floods occurred due to dangerous hydro-meteorological phenomena in Galati and Vaslui counties, Romania", starting 14 Sep 2024 05:00. A CEMS Risk and Recovery activation EMSN193 (Tazlau river, opened 7 May 2024) produced extent/depth/velocity for one river; Tazlau is in the Siret basin, not Galati. Other R&R work for Galati: not found.
    - Source: https://mapping.emergency.copernicus.eu/news/flood-in-galati-and-vaslui-counties-romania/
    - Quote: "major floods occurred due to dangerous hydro-meteorological phenomena in Galati and Vaslui counties, Romania."
    - Source date: 2024-09-14
    - Source type: official docs
    - Confidence: high (event); low (EMSN193 details from search summary)
24. **Claim:** JRC pan-European pluvial or coastal hazard layers: not found in this search; not evaluated.
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

## Relevance to LandHorizon
- **JRC v3 depth rasters are the only candidate that fits the pipeline as-is.** Free GeoTIFF over HTTP, no account, nine return periods, CC BY 4.0 per copyright.txt (or ODbL per README, unresolved: ask JRC or check before redistributing a derived raster, because ODbL share-alike could apply). Work needed: a ranged read or one-off download of the files (260-334 MB each, ~2.7 GB for nine), clip to the Galati AOI, convert to COG, keep one band per RP. About half a day of work, no meaningful compute. No new dependency (rasterio/GDAL already needed).
- **But it is coarse and blind to our flood type.** ~90 m cells (v2: 100 m) means a 1 ha plot is 1-2 cells, so it describes the area, not the plot. It models only rivers above a catchment threshold (500 km2 in v2; v3 threshold not found; small channels under 3,000 km2 are flagged as spurious-depth areas). The September 2024 Galati event hit small streams, so the layer would probably show "no hazard" there. Per project rules that must be returned as `unknown`/"not modelled", never low risk. Defences (Danube, Siret dikes) are not represented in v2, so the layer overstates hazard behind dikes. No Romanian validation was found.
- **Open item that can block use:** the v3 README extent (to 27.81 degrees) may exclude Galati at about 28.0 E (claim 7). Check the GeoTIFF header first; it takes minutes.
- **Romanian RO-FLOODS maps are the better content (LiDAR-based, depth, 10/1/0.1 % probable scenarios, the same source Imoreview uses) but the access terms are unclear.** Only a web viewer is confirmed; an INSPIRE WMS and an EEA registry entry "View and Download Service / Freely accessible" exist, but no licence text and no confirmed bulk download were found. Scraping a viewer is not a licence. Recommended next step for the team: ask ANAR/INHGA (and read the WMS GetCapabilities AccessConstraints) for the licence and GIS files. Until then do not build on it; if WMS use is allowed, a WMS can be rasterized once into a COG (GetMap at fixed resolution) in the batch pipeline. Cost: team time for the request, no money.
- **EFAS is not a plot-level layer.** It gives discharge at ~1.5 km (1 arcmin) river points, not inundation; real-time is partner-only (30-day embargo), archives are open. At most it could supply a return-period flow, which the team cannot turn into a map without running a hydraulic model (out of scope). Not recommended; mention as roadmap.
- **Pitch/roadmap:** "modelled hazard from RO-FLOODS, with licence agreed with ANAR" is a credible roadmap item. RO-FLOODS III (Cycle III maps) is being tendered in 2026, so the data may change soon.
- **Competitor:** Imoreview checks an address point against RO-FLOODS and admits a point does not describe a plot. LandHorizon's plot-level polygon sampling plus observed history is a differentiator; copying their layer adds parity, not advantage.
- Time and people: the JRC route fits the 22 Nov gate only as a small add-on; given the freeze on 6 Dec and the existing GFM decision, treat any modelled layer as optional.

## Open questions
- Does the v3 JRC raster cover Galati (about 45.43 N, 28.05 E)? And what is the v3 minimum catchment? Read the TIF header and ask JRC.
- ODbL (README) vs CC BY 4.0 (copyright.txt): which governs? Check the JRC Data Catalogue entry (blocked for my tool).
- Exact RO-FLOODS scenarios, grid resolution, and the pluvial/flash-flood treatment: read the World Bank 2024 report "Planning for Flood Resilience in Romania" (403 for my tool).
- ANAR WMS GetCapabilities URL and its AccessConstraints; whether INSPIRE download service or GIS files exist; Law 179/2022 and Regulation (EU) 2023/138 on high-value datasets.
- Imoreview's Terms and "Date si surse" page (not read).
- Out of bounds, one line: GloFAS global hazard maps and Flood Hub are covered by other researchers.
- No instructions embedded in fetched content were observed.

## Review
Reviewed: 2026-11-11 to 2026-11-12 (interrupted by a usage limit, then resumed). The reviewer did not write this file.

Method limit: sources were opened through a fetch tool that answers questions about the page and caps quotes at about 125 characters. Each quote was checked by asking whether the exact string is on the page. No raster and no PDF/DOCX body was read. Nothing was downloaded or run.

Count: 14 verified, 5 unsupported, 2 misquoted, 3 unreachable.

### Verdicts
1. `verified`. All three quotes are in the README ("G01. Dataset version 3.1.1", "D02. Horizontal resolution: 3 arc seconds (~90 m)", "for nine different flood return periods"). The README does not list the nine periods; they and the sizes (260M to 334M) come from the directory listing, which I opened and which matches. Note: the listing shows README.txt modified 2026-10-21 while its own text says "Last update of the README file: 05.03.2026".
2. `verified`. Changelog headers read "V3.1.1 (2026-03-05)", "V3.1.0 (2024-11-08)", "V3.0.0 (2024-03-08)", "v2.0.0 (2022-04-26)", "v1.0.0 (2014-01-13)". The artefact sentence and the README "Manuscript under preparation." line are there. A search on 2026-11-12 found no published Baugh et al. paper.
3. `verified`, with a limit on the wording. The changelog says the file "identifies areas where depths >10m are predicted in small channels (<3,000km^2)" for the 10-year return period, plus a 2 km buffer, and "Users should exercise caution when using the depth values in these areas." That flags specific places with implausible depth. It does not mark all small-channel results as unreliable, which is how the claim's "i.e." and the relevance section read it.
4. `verified`. All three quotes are in the ESSD paper (Sect. 2.2, Sect. 2.3, abstract). The v3 README has no line on minimum upstream area or defences (checked).
5. `verified`. Quote is in the abstract. The paper names "official hazard maps for Hungary, Italy, Norway, Spain and the UK"; CSI values "approach and in some cases exceed 0.5 for return periods equal to or above 500 years"; Hungary "FAR is very high for the 1-in-30-year flood map"; Norway "general tendency to overestimate flood extent"; England "tend to underestimate flood extent". Romania is not a validation area.
6. `verified`. README: "A02. License information, restrictions on use: Open Data Commons Open Database License v1.0". copyright.txt: licensed under CC BY 4.0, "Reuse is allowed provided appropriate credit is given and any changes are indicated." The two files do disagree. The share-alike remark about ODbL is the researcher's reading, not from a cited source.
7. `unsupported`. The quote is exact ("D01. Horizontal coverage: European extended domain (-24.54, 67.26; 27.81, 71.13)", no axis labels). It does not support "taken literally this would stop at about 27.8 E". For 27.81 to be the eastern edge, the latitude range would have to be 67.26 to 71.13, which is only the far north of Scandinavia. The only reading that gives a European map is longitude -24.54 to 67.26 and latitude 27.81 to 71.13, which puts Galati (45.43 N, 28.05 E) inside. That is my reasoning, not a confirmed fact: read the GeoTIFF header before relying on either reading.
8. `misquoted`. "The hydrological input is at 5 km and daily resolution." is not in the paper. The actual text is "run a long-term hydrological simulation for the period 1990–2016 at 5 km grid spacing and at daily resolution". The EFAS link is in the paper as "developed as a component of the Copernicus European Flood Awareness System (EFAS". The facts hold; the quote has to be replaced before the claim is used.
9. `verified`. Both quoted strings are on the page ("2 EFAS products overview"; the source uses curly quotation marks). The page is dated: last modified 26 Feb 2026, not "undated". It says other EFAS products are public in real time; it does not mention historical data, so that half of the claim rests on claim 12.
10. `verified`. "1x1 arcminute for version 5.0, 5x5km for version 4.0 and older" (the source has no final full stop), "The real-time data is only available to EFAS partners." and "with a 30-day delay" are on the page. Licence label "CEMS-FLOODS datasets licence". Publication date shown: 2019-05-09.
11. `unsupported`. The resolution quote is exact. The second quote is cut: the sentence continues ", which are used as criteria for issuing notifications." The Auxiliary Data download is confirmed. But neither quote supports the headline "EFAS produces discharge, not inundation", and the claim 9 source links a product called "EFAS Rapid Flood Mapping and Rapid Impact Assessment" (see Missed 1).
12. `unsupported`. The researcher gave no quote and did not open the page. I opened it on 2026-11-12: "For the latest version data is available from 1992-01-01 up until near-real time.", licence "CEMS-FLOODS datasets licence", "The real-time data is only available to EFAS partners." The page does not state "free account" and does not cover reforecasts (a separate dataset). The claim needs to be rewritten with these quotes before use.
13. `verified`. All quoted strings are on the World Bank page, as are "526" APSFRs, annual exceedance probabilities and a climate-change scenario. The page shows no date of its own (2023-03-22 is from the URL), no grid resolution, no licence and no download.
14. `misquoted`. The source says "Hărţile, care sunt accesibile oricărei persoane interesate", not "accesibilă". One letter, same meaning, but the quote was altered. "disponibile pe www.inundatii.ro" is exact; date 7 Nov 2022, World Bank, 11 basin administrations and the September submission to the Commission are confirmed. INHGA is not in the article: it names only the Ministry and Administraţia Naţională "Apele Române". The article's "Vizualizator Web GIS" refers to preliminary maps uploaded for expert review, not clearly to the public site.
15. `verified`. The Imoreview sentence is exact. I also opened https://inundatii.ro/ : its home page lists no 10 % / 1 % / 0.1 % scenarios, no licence, no download and no WMS, and its link to the maps is malformed ("https:///harticiclul2.inundatii.ro"). The percentages remain single-source, from a competitor.
16. `verified`. The mediafax quote is exact (published 24 Apr 2014, updated 31 Mar 2020). The World Bank string "fluvial flooding, flash floods, pluvial and coastal flooding" and the Imoreview string are on their pages. The World Bank sentence is about methodologies developed, not about what was published for Galati, so the conflict is real and unresolved.
17. `unsupported` as written. Only this part is confirmed: EEA CIS2 record 915 "Flood Hazard and Risk Maps", provider "Inundatii.RO" (Distributor), "Freely accessible", "View and Download Service", format "Multiple", no licence, no URL (created 11 Mar 2026, modified 15 May 2026). The record does not mention ANAR, so "two datasets" is not shown by the cited source. The WMS is not confirmed: a search returned an INSPIRE Geoportal record "RO.ANAR / NZ.ZoneInundabile.WMS" dated 2019-06-06, but the geoportal did not resolve and the GetCapabilities URL it lists returned 404 (see Missed 4).
18. `verified`. The quote is exact and continues "and the official Flood Zones datasets provided by the Romanian Water National Administration (ANAR)". No access conditions or licence. Page published 06 May 2026; it concerns activation EMSN193 (Tazlău basin), not Galați.
19. `unreachable`. The .docx came back as undecodable binary. The title and the transposition were not confirmed from this source.
20. `unreachable`. The TED PDF body could not be decoded and the HTML notice page returned empty. Nothing about RO-FLOODS III was confirmed.
21. `verified`. "Poziția adresei este comparată cu hărțile oficiale RO-FLOODS." and "Verificarea unui punct nu descrie fiecare colț al parcelei, subsolul sau cota pardoselii." are on /inundatii, which links RO-FLOODS to https://inundatii.ro/ and reports "scenariul și adâncimea estimată disponibilă". The string "Zone inundabile: Hărțile oficiale de hazard, pe adresă" is not on the cited page: it is on the home page (https://imoreview.ro/) as two separate elements, without the colon. "Gratuit, fără cont." is also on the home page. No licence statement on either page.
22. `unreachable`. HTTP 403.
23. `verified` for the event: the quote is exact, the sentence starts "On 14 September 2024, starting at 05:00 local time", activation EMSR758. The cited page does not mention EMSN193. The claim 18 source confirms EMSN193 was activated on 07 May 2024 for the Tazlău River basin; that EMSN193 itself produced extent, depth and velocity was not confirmed.
24. `unsupported`. No source and no quote, so there is nothing to check. It is a "not found" note, not a finding.

### What the researcher missed
1. **EFAS does have an inundation product.** The EFAS wiki has a page "EFAS Rapid Flood Mapping and Rapid Impact Assessment" (last modified 16 Dec 2024) that points to "Dottori et al., 2017" for the method. A search summary says it maps forecast discharge to a catalogue of return-period inundation maps at 90 m, in an "unprotected" scenario; I could not confirm that wording on the page itself. It is an event forecast layer, not a static hazard map, so the conclusion "not a plot-level layer" stands, but "discharge, not inundation" is too absolute. https://confluence.ecmwf.int/spaces/CEMS/pages/265028472/EFAS+Rapid+Flood+Mapping+and+Rapid+Impact+Assessment
2. **Flood maps look like high-value datasets under EU law.** Implementing Regulation (EU) 2023/138 lists "Natural risk zones (III)" among the INSPIRE themes in the Earth observation and environment category and requires a "Creative Commons BY 4.0 licence or any equivalent or less restrictive open licence", made available "through APIs and bulk download". It applies "from 16 months after entry into force" (about June 2024, my calculation). Whether the RO-FLOODS maps fall under it and whether ANAR complies was not found, but this is the argument to use when asking ANAR. https://eur-lex.europa.eu/eli/reg_impl/2023/138/oj
3. **The EFAS licence was readable.** "CEMS-FLOODS datasets licence (rev. 1)" grants free access for "(a) reproduction; (b) distribution; (c) communication to the public; (d) adaptation, modification and combination with other data and information", requires the credit "Generated using Copernicus Emergency Management Service information [Year]", and says the data are "provided for information purposes only". Commercial use is not named either way. https://ewds.climate.copernicus.eu/licences/cems-floods
4. **The ANAR WMS endpoint is dead for now.** The URL listed by the 2019 INSPIRE record returned 404 on 2026-11-12, so no AccessConstraints could be read and "an INSPIRE WMS exists" is unconfirmed. https://portal-gis.rowater.ro/inspire/rest/services/INSPIRE/NZ_View/MapServer/exts/InspireView/service?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetCapabilities
5. **No independent validation of v3 exists in this file.** The only validation cited is of v2 (100 m, different hydrology, 500 km2 threshold). v3 has a different resolution and inputs and its paper is unpublished, so v2 skill, the v2 catchment threshold and the v2 "no defences" statement cannot be carried over to the files we would download. https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/CHANGELOG.txt
6. **The JRC Data Catalogue entry is still unread.** It rejected my request too ("The requested URL was rejected"), so the licence conflict in claim 6 and the v3 description stay open. https://data.jrc.ec.europa.eu/dataset/1d128b6c-a4ee-4858-9e34-6210707f3c81
7. **A sibling JRC README may settle the axis order of claim 7.** A search summary reports the EFAS static-maps README gives the same domain as "(-25.25, 50.25; 22.75, 72.25)", which only makes sense as longitude range then latitude range. I could not open it (404), so this is not confirmed. https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/LISFLOOD_static_and_parameter_maps_for_EFAS/README.txt

### Problems in "Relevance to LandHorizon"
- **"The September 2024 Galati event hit small streams, so the layer would probably show 'no hazard' there."** No claim supports "small streams": claim 23 only says "dangerous hydro-meteorological phenomena". The v3 catchment threshold is also "not found" (claim 4). This is a guess and should not go into a synthesis. https://mapping.emergency.copernicus.eu/news/flood-in-galati-and-vaslui-counties-romania/
- **"small channels under 3,000 km2 are flagged as spurious-depth areas"** overstates claim 3. Only places where the 10-year depth exceeds 10 m (plus a 2 km buffer) are flagged. https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/CHANGELOG.txt
- **"the layer overstates hazard behind dikes"** applies a v2 statement to v3. Claim 4 itself rates that as low confidence. https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
- **"Open item that can block use" (27.81 degrees)** rests on claim 7, which is unsupported. The header check is still worth its few minutes, but the item should not be presented as a likely blocker. https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/CEMS-EFAS/flood_hazard/README.txt
- **Return periods and the "not a probability" rule.** constraints.md says the product is a screening indicator, "not a probability", and must not claim return periods from our own data. The section proposes "one band per RP" without saying how nine return-period depths would be shown. If used, they have to be labelled as a third-party model output, separate from our observed history.
- **Evidence contract.** A modelled-hazard field changes the Pydantic contract in `api/main.py`, which needs the lead's review. The section does not mention it, and "about half a day" does not include the API, the frontend or the tests. That estimate is not backed by any claim.
- **RO-FLOODS as "the better content" with "10/1/0.1 %" scenarios** rests on claim 15 (one competitor page). "An INSPIRE WMS ... exist" rests on claim 17, which is unsupported. Rasterizing a WMS GetMap gives styled pictures, not depth values (my reasoning, no source), so that route would give extent classes at best.
- **"RO-FLOODS III ... is being tendered in 2026"** rests on claim 20, which is unreachable. It should not be used in the pitch until someone reads the notice. https://ted.europa.eu/it/notice/420756-2026/pdf
- **"EFAS ... archives are open"** rests on claim 12 (unsupported as filed). The licence in Missed 3 backs open access but does not name commercial use.
- Respected: missing or not-modelled data returned as `unknown`, free data only, no new dependency (`rasterio` is already in `pyproject.toml`), one 1 ha plot is about 1 to 2 cells at about 90 m, and the size total (the nine files add up to about 2.7 GB).

### Instructions in fetched content
None found. The fetch tool sometimes suggested next steps (for example "paste the text"); those are tool output and were ignored.
