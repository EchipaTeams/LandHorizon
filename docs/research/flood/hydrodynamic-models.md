# What would running a high-resolution hydrodynamic flood model (LISFLOOD-FP and alternatives), or reusing its outputs, take for LandHorizon, and is it more than a roadmap item?
Date: 2026-11-11
Scope: In: LISFLOOD-FP, JBA Flood Foresight, the FFWC "Super Model", open alternatives and terrain baselines (HAND first), Romanian modelling studies and fine-resolution elevation data. Out (other researchers): hazard-map products as products (GloFAS, Flood Hub, EFAS, JRC maps, RO-FLOODS/ANAR), ML surrogates, Sentinel-1/GFM observed mapping. Quotes come from pages fetched on 2026-11-11. Fetch tool output is partly summarised, so reviewers should recheck each quote.

## Claims

### 1. LISFLOOD-FP
1. **Claim:** LISFLOOD-FP is a 2D hydrodynamic floodplain inundation model from the University of Bristol, and the Bristol page itself calls it a "non-commercial, research code".
   - Source: https://www.bristol.ac.uk/geography/research/hydrology/models/lisflood/
   - Quote: "a two-dimensional hydrodynamic model specifically designed to simulate floodplain inundation"
   - Source date: undated page, fetched 2026-11-11
   - Source type: official docs
   - Confidence: medium (the "non-commercial" wording is the fetch tool's paraphrase, not a verified quote; the quote above is the model description)

2. **Claim:** Current release is LISFLOOD-FP 8.2 (GMD, 10 Dec 2025), open source under GPL v3.0. The earlier 8.0 paper also states GPL v3. GPL allows commercial use but requires source disclosure for distributed derivatives. This differs from the old Bristol "non-commercial" wording, so the version matters.
   - Source: https://gmd.copernicus.org/articles/18/9827/2025/
   - Quote: "The LISFLOOD-FP 8.2 code is open source, under the GPL v3.0 licence"
   - Source date: 2025-12-10
   - Source type: peer-reviewed
   - Confidence: high
   - Second source: https://gmd.copernicus.org/articles/14/3577/2021/ , quote "LISFLOOD-FP 8.0 is freely available under the GPL v3 license" (2021, peer-reviewed). The Zenodo DOI for 8.2 is not confirmed (a search snippet showed two different DOIs; not found in an opened page).

3. **Claim:** Version 8.x has CPU and GPU solvers. GPU runs are far faster on big grids; the 8.0 paper finds GPU solvers most efficient above 1 million cells. A 50 km x 50 km domain at 30 m is about 2.8 million cells, in the GPU-favourable range (my arithmetic).
   - Source: https://gmd.copernicus.org/articles/14/3577/2021/
   - Quote: "the GPU solvers are 2.5–4 times faster than the corresponding 16-core CPU solvers"
   - Source date: 2021
   - Source type: peer-reviewed
   - Confidence: medium (the GPU-speed-up quote is verified; the cell count is my arithmetic)

4. **Claim:** For the local-inertial (ACC) solver on GPU the speed-up over CPU is 2-28x depending on case; the catchment test cases were 1180 km2 and 2500 km2 on a consumer-class GPU. No absolute wall-clock runtime for a 50 km x 50 km, 30 m domain was found: "not found". The paper text reports ratios only (runtimes sit in an image table).
   - Source: https://gmd.copernicus.org/articles/16/2391/2023/
   - Quote: "the uniform ACC solver is found to be 2–28 times faster than the CPU predecessor"
   - Source date: 2023
   - Source type: peer-reviewed
   - Confidence: medium

5. **Claim:** Input set is: DEM, floodplain friction map, river bed elevation and river width maps (or sub-grid channel), a boundary-condition file (.bci), time-varying boundary file (.bdy), optional rainfall and infiltration, and a parameter file (.par). Source is a university training exercise, not the manual itself.
   - Source: https://hydroeurope.upc.edu/wp-content/uploads/2024/11/HydroEurope_Unceratinty_Analysis.pdf
   - Quote: not captured (the source was seen only as a search snippet and not opened by me). Do not use until a reviewer opens it. Manual to read instead: https://btphillips94.github.io/lisflood-notebook/user_manual.pdf (also not opened).
   - Source date: 2024
   - Source type: official docs (training material)
   - Confidence: low

6. **Claim:** Published pan-European JRC hazard maps are made with LISFLOOD-FP at 100 m, but they exclude local flood defences, use a DEM that is not public, and only simulate rivers with more than 500 km2 upstream area. This is the "made with LISFLOOD-FP" link; product details are for another researcher.
   - Source: https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
   - Quote: "inundation simulations are performed with the hydrodynamic model LISFLOOD-FP" ; "the flood maps developed do not account for the influence of local flood defences" ; "The CCM DEM dataset used in this research is not publicly available."
   - Source date: 2022-04-07
   - Source type: peer-reviewed
   - Confidence: high (quotes as returned by the fetch tool; the 500 km2 limit was reported as a paraphrase)

7. **Claim:** JRC validation of LISFLOOD-FP at continental scale: the maps identify about two-thirds of reference flood extent at 1-in-100-year and overestimate below that. This gives a realistic accuracy ceiling for a regional LISFLOOD-FP chain without local calibration.
   - Source: https://essd.copernicus.org/articles/14/1549/2022/essd-14-1549-2022.html
   - Quote: "the modelled maps can identify on average two-thirds of reference flood extent"
   - Source date: 2022-04-07
   - Source type: peer-reviewed
   - Confidence: high

8. **Claim:** A global-DEM LISFLOOD-FP study found a FABDEM-based model consistently beat a MERIT-based one (Vietnam, 3 sites, CSI 37-62 % against household data, >0.8 against remote sensing at peak for two sites). This is not flat or embanked terrain, and no head-to-head GLO-30 vs FABDEM LISFLOOD-FP test in a flat, embanked floodplain was found: "not found".
   - Source: https://nhess.copernicus.org/articles/24/539/2024/
   - Quote: "The global flood model based on FABDEM consistently outperformed a model based on MERIT"
   - Source date: 2024-02-15
   - Source type: peer-reviewed
   - Confidence: medium

9. **Claim:** GLO-30 is a surface model (includes buildings and vegetation); its errors can act as artificial barriers or sinks; satellite DEMs cannot resolve levees. FABDEM is a bias-corrected derivative of GLO-30. Evidence here comes from search results (not opened by me), so it is listed as a lead only.
   - Source: https://iopscience.iop.org/article/10.1088/1748-9326/ac4d4f
   - Quote: not captured (not opened by me)
   - Source date: 2022
   - Source type: peer-reviewed
   - Confidence: low

10. **Claim:** Boundary-condition discharges for Danube/Siret/Prut: the only openly fetched candidates were GRDC (Ceatal Izmail, Danube mouth, GRDC ID 6742900, far downstream of Galați), which needs identified access and has no API, and PANGAEA monthly Ceatal Izmail data (CC BY 3.0, 1921-1984, monthly only, from a search snippet). No open daily Siret or Prut station source was found. Reanalysis or forecast discharge (GloFAS, EFAS) is the practical free route and is covered by another researcher.
    - Source: https://grdc.bafg.de/help/faq/
    - Quote: "This requires an identified access to hydrological data."
    - Source date: undated, fetched 2026-11-11
    - Source type: official docs
    - Confidence: medium

### 2. JBA Flood Foresight
11. **Claim:** Flood Foresight is a commercial flood forecasting system from JBA. By JBA's own description it provides rainfall severity, flood inundation footprints and depth, and impacts. Everything here rests on JBA alone.
    - Source: https://www.jbaconsulting.com/2023/10/05/delivering-global-flood-mapping-solutions/
    - Quote: "a globally-scalable solution providing rainfall severity, flood inundation footprints and depth, and flood impacts"
    - Source date: 2023-10-05
    - Source type: vendor
    - Confidence: medium

12. **Claim:** JBA says it is deployed in over 20 countries and territories, for humanitarian anticipatory action, disaster risk financing and parametric insurance. No statement about free or open access and no price were found.
    - Source: https://www.jbaconsulting.com/?p=13138
    - Quote: "over 20 countries and territories"
    - Source date: 2025-10-07 (from URL, no explicit date on page)
    - Source type: vendor
    - Confidence: medium

13. **Claim:** The JBA product page offers no pricing and says nothing free or open; access is by contacting JBA. Whether Romania is a covered country: "not found". The 30 m figure in JBA's global flood map is stated by JBA for its map product.
    - Source: https://www.jbaconsulting.com/?p=741
    - Quote: not applicable (absence of pricing; page says it "provides near-real-time and forecast rainfall and flood data")
    - Source date: undated
    - Source type: vendor
    - Confidence: medium

### 3. FFWC "Super Model"
14. **Claim:** The FFWC is Bangladesh's national flood forecasting centre; its forecasting system is based on the MIKE 11 (DHI) 1D model, with 2D inundation depth forecasts made from 300 m DEMs and a 120 h lead time. It is a national operational system for Bangladesh river basins.
    - Source: https://nhess.copernicus.org/articles/21/1807/2021/
    - Quote: "The FFWC's flood forecasting system is based on the MIKE 11 model,"
    - Source date: 2021
    - Source type: peer-reviewed
    - Confidence: high for MIKE 11; the exact name "Super Model" was not found in any page I opened.

15. **Claim:** The newer FFWC system (Oct 2025) is built on MIKE+ with a rainfall-runoff module over 247 Bangladeshi catchments. This is tied to Bangladesh's catchments and gauging network.
    - Source: https://www.tbsnews.net/node/1269886
    - Quote: "the MIKE+ one-dimensional hydrodynamic model"
    - Source date: 2025-10-26
    - Source type: blog (news article)
    - Confidence: medium

16. **Claim:** A University of Reading paper compares the "Super Model" with global systems for the July 2020 Jamuna flood. I could only see this in search snippets (the PDF returned Access Denied), so it is not cited: not found (opened).
    - Source: https://centaur.reading.ac.uk/113412/8/nh0541115.pdf
    - Quote: not available (access denied)
    - Source date: unknown
    - Source type: peer-reviewed
    - Confidence: low

### 4. Open alternatives (one line each)
17. **Claim:** HAND-based inundation vs 2D hydraulic models: one comparison (Huron Creek, Michigan, 1000-year rainfall event) finds comparable extent but variable agreement, driven by synthetic rating-curve uncertainty. HAND needs only DEM plus rating curve. No quantitative score in the abstract.
    - Source: https://digitalcommons.mtu.edu/michigantech-p2/439
    - Quote: "the HAND model produces different degrees of concurrence in both flood inundation extent and depth"
    - Source date: 2024-01-13
    - Source type: peer-reviewed
    - Confidence: medium

18. **Claim:** A 2025 GMD paper finds the simple HAND-Manning method is far worse than an improved dynamic HAND (DHAND) with a 1D solver, which in turn beats HEC-RAS 1D against a 2D benchmark. So plain HAND is a cheap, rough baseline.
    - Source: https://gmd.copernicus.org/articles/18/3387/2025/
    - Quote: "vastly outperforms the simpler HAND–Manning method"
    - Source date: 2025-06-12
    - Source type: peer-reviewed
    - Confidence: medium
    - Not found: HAND vs LISFLOOD-FP numbers (the Paris 2016 EGU abstract PDF could not be read).

19. **Claim:** SFINCS (Deltares): reduced-physics fast flood model, source GPL v3.0 (commercial use allowed); pre-built Windows/Docker binaries under a separate freeware licence without redistribution or modification. Latest release in the docs is v2.4.0.
    - Source: https://github.com/Deltares/SFINCS
    - Quote: "This source code is available open source under GNU GPL-3.0 license, see attached."
    - Source date: fetched 2026-11-11
    - Source type: official docs
    - Confidence: high
    - Speed: "Designed to run in minutes instead of days" (https://sfincs.readthedocs.io/en/latest/index.html, vendor-style claim, official docs). Inputs and hardware not captured.

20. **Claim:** HEC-RAS 2D: free to use, executable is US public domain, supports 2D unsteady flow and rain-on-grid, version 7.0.2 current on the download page; Windows-first.
    - Source: https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS%205.0%202D%20Modeling%20Users%20Manual.pdf
    - Quote: "The HEC-RAS executable code and documentation was developed with U.S. Federal Government resources and is therefore in the public domain."
    - Source date: 2016 (v5.0 manual)
    - Source type: official docs
    - Confidence: medium (quote came from a search result summary, not opened by me; the HEC product page I opened did not state licence)

21. **Claim:** ANUGA is open-source shallow water software with a GPU/multicore solver, installable via conda. Licence name not confirmed (README points to LICENSE.txt).
    - Source: https://github.com/anuga-community/anuga_core
    - Quote: "ANUGA (pronounced "AHnooGAH") is open-source software for the simulation of the shallow water equation"
    - Source date: fetched 2026-11-11
    - Source type: official docs
    - Confidence: medium

22. **Claim:** Itzi is a GPL (2.0) dynamic flood model that requires GRASS GIS 8.5 or above installed first.
    - Source: https://github.com/ItziModel/itzi
    - Quote: "Itzï is released under the GPL license."
    - Source date: fetched 2026-11-11
    - Source type: official docs
    - Confidence: medium

23. **Claim:** TELEMAC is GPL v3 free software (EDF page, via search summary; official page not opened). Heaviest set-up of the options (unstructured mesh, Fortran suite). GeoFlood and FLDPLN: not found (GitHub URL returned 404; no source opened). Planar "bathtub" fill: no source retrieved: not found.
    - Source: https://www.edf.fr/en/the-edf-group/inventing-the-future-of-energy/r-d-global-expertise/our-offers/simulation-softwares/opentelemac
    - Quote: not captured (not opened)
    - Source date: unknown
    - Source type: vendor
    - Confidence: low

### 5. Romanian context
24. **Claim:** Published local hydraulic modelling of the lower Siret and Prut exists (1D HEC-RAS Siret-Danube confluence reach by Galați authors; 2D HEC-RAS for the Prut downstream of Stânca-Costești, four events). Only seen in search results; none of the papers could be opened (403 or unreadable PDF), and no data availability or reusable model files were found: "not found". Papers cited for review: https://mdpi.com/2071-1050/12/16/6588/htm and https://aerapa.conference.ubbcluj.ro/2024/pdf/51_64_Urzica_etal_AWC_2024.pdf .
    - Source: https://mdpi.com/2071-1050/12/16/6588/htm
    - Quote: not available (403)
    - Source date: 2020
    - Source type: peer-reviewed
    - Confidence: low

25. **Claim:** ANCPI national DTM (Romania Elevation Model): 5 m and 20 m versions on a third-party wiki, built from 1:50,000 contours (1995 map, some areas updated to 2019); ANCPI vertical accuracy stated as 1.5 m for flat areas; licence OGL ROU 1.0. This is coarse and contour-derived, not LiDAR. Excludes part of the Danube delta (Tulcea, NE Constanța).
    - Source: https://help.emd.dk/mediawiki/index.php/Romania_Elevation_Model
    - Quote: "Open Government License - OGL ROU 1.0" ; "1.5m for flat areas"
    - Source date: 2024-07-03 (page edited; data status June 2024)
    - Source type: blog (third-party wiki relaying ANCPI)
    - Confidence: medium

26. **Claim:** LAKI III 0.5 m LiDAR DTM public coverage is currently Zone A (Caraș-Severin, Gorj, Mehedinți, Dolj); Zone B (Suceava, Neamț, Bacău, Vrancea) is next. Galați is in neither list. Other public models are mostly 1-2 m products and about 5 m locally. Licence of LAKI data not stated in the source.
    - Source: https://arxiv.org/html/2606.08876v1
    - Quote: "LAKI III Zone B, comprising Suceava, Neamţ, Bacău, and Vrancea counties, is the next scheduled high-resolution extension."
    - Source date: 2026-06-07
    - Source type: preprint
    - Confidence: medium (whether Galați has any open 1-2 m DTM: not found)

## Relevance to LandHorizon
- **Verdict:** a LISFLOOD-FP (or SFINCS/HEC-RAS 2D) model of the Galați confluence is a **roadmap item, not buildable by 6 Dec**. The honest "dead end for the sprint" reasons come from the sources above:
  - There is no free daily Siret/Prut discharge series (claim 10); the free reanalysis route is covered elsewhere.
  - The only terrain in the pipeline is GLO-30, a surface model that cannot resolve levees (claim 9, lead only), and Galați is a diked floodplain. JRC's own LISFLOOD-FP maps ignore defences (claim 6) and capture about two-thirds of reference extent (claim 7).
  - No source gives an effort estimate for a first set-up. My own estimate, labelled as such: a first calibrated run needs several weeks for one person (data acquisition, channel geometry, defences, calibration, validation against an independent sensor), which exceeds what 1-2 flood people can spare from about 280-350 total person-hours.
- **Licence:** LISFLOOD-FP 8.x and SFINCS source are GPL v3, so commercial use is permitted (claims 2, 19). The SFINCS Windows binary is freeware without redistribution (claim 19). HEC-RAS is free (claim 20). Older LISFLOOD-FP versions were described as non-commercial; do not use one.
- **Compute:** a 50 km x 50 km domain at 30 m is about 2.8 million cells (my arithmetic). GPU solvers are designed for that size (claim 3). Absolute runtimes: not found. A free-tier Colab or similar GPU may suffice, but this was not checked.
- **Cheap baseline in the pipeline:** HAND from GLO-30 already exists. Published comparisons show HAND gives comparable extent in data-scarce settings but variable depth and sensitivity to the rating curve (claims 17, 18). It can be presented honestly as a "terrain-based susceptibility screen", not a hydrodynamic result. No comparison with LISFLOOD-FP numbers was found.
- **Reusing published outputs:** the JRC LISFLOOD-FP maps are the only reusable hydrodynamic output found, with the defences and 100 m limits above (claim 6); product terms are for another researcher.
- **Flood Foresight:** commercial, vendor-only evidence, no price, no free tier found, Romanian coverage not found (claims 11-13). Not usable by a student team; at most a competitor note for the pitch.
- **FFWC "Super Model":** Bangladesh-specific national MIKE 11 forecasting system built on Bangladeshi river network and gauges (claims 14, 15). Not transferable to Romania; no reusable output or method found beyond the general fact that 1D hydrodynamic models are fed by gauged boundaries. A dead end for us.
- **Romanian data:** national DTM is 5 m contour-derived under OGL ROU 1.0 (claim 25), finer than GLO-30 on paper but only 1.5 m vertical accuracy in flat areas. LiDAR for Galați: not found. Neither could be checked for the diked floodplain at plot scale.
- **Pitch use:** a roadmap slide can honestly say "calibrated 2D hydrodynamic model with levee data and gauged inflows (SFINCS/LISFLOOD-FP), requires ANAR/INHGA gauge data and defence geometry that are not open".

## Open questions
- Does Apele Române / INHGA publish daily Siret, Prut and Danube (Galați) discharge or defence crest elevations openly? Not found.
- Is any 1-2 m LiDAR DTM open for Galați county, and what is its licence? Not found.
- Absolute LISFLOOD-FP or SFINCS runtimes for a 30 m, about 2,500 km2 domain: not found (GMD tables are images).
- Direct HAND vs LISFLOOD-FP quantitative comparison (Paris 2016, EGU 2018): PDF unreadable, not found.
- Original source of the "Super Model" name (BWDB/FFWC or DHI report): only seen in unopened search snippets.
- Out of bounds, one line each: JRC/EFAS/GloFAS hazard maps as products; RO-FLOODS/ANAR maps.

## Review
Reviewed: 2026-11-11 to 2026-11-12, by a reviewer who did not write this file.
Method: every cited URL was opened with the fetch tool. The tool returns short quoted pieces and summaries, so "quote present" means the tool confirmed the exact phrase on the page, not that I read the raw HTML. PDFs could not be read here (no PDF text extraction). A claim with several parts gets one verdict; the note says which parts are safe to use.

Count: 18 verified, 3 unsupported, 0 misquoted, 5 unreachable.

### Verdicts
1. `verified`. The quote is on the Bristol page. The page also contains "It is a non-commercial, research code developed as part of an effort to improve our fundamental understanding", so the "non-commercial" wording is a real quote, not a paraphrase. The page has no date, no version number and no licence text.
2. `unsupported`. Both quotes are exact (8.2 abstract, GMD 18, 9827, 10 Dec 2025; 8.0 abstract, GMD 14, 3577, 11 Jun 2021). Two parts of the claim fail:
   - "Current release is 8.2" is out of date. The 8.2 Zenodo record says "There is a newer version of the record available", and its latest link shows "LISFLOOD-FP 8.3 hydrodynamic model", published 13 Oct 2026 (https://zenodo.org/records/13121102/latest).
   - The licence is inconsistent between primary sources. The papers say GPL v3; the Zenodo records for 8.2 and 8.3 both show the licence field "GNU General Public License v2.0 only" (https://zenodo.org/records/13121102). Which one applies has to be read from the licence file inside the code archive, which I did not open.
   - The 8.2 code DOI the researcher could not confirm is given in the paper's code availability section: 10.5281/zenodo.13121102.
3. `verified`. Both statements are in the 8.0 abstract: "the GPU solvers are 2.5–4 times faster than the corresponding 16-core CPU solvers" and "The DG2-GPU and FV1-GPU solvers are most efficient on grids with more than 1 million elements". They are about the DG2 and FV1 solvers, not the ACC solver. The arithmetic is right (about 2.78 million cells).
4. `verified`. The quote is in the 8.1 abstract (GMD 16, 2391, 5 May 2023). The page gives Upper Lee as 1180 km2 and Eden as 2500 km2, a third case of 14.84 km2, and the GPU as "Nvidia Quadro RTX 2070 SUPER". "Consumer-class" is the researcher's wording. I did not check the runtime tables, so the "not found" stands unchecked.
5. `unreachable`. The PDF downloads but its text could not be read here. The researcher gives no quote. Not usable.
6. `unsupported` as written. The quotes are in the 2022 ESSD paper, and the 100 m and 500 km2 figures are confirmed there. Two problems:
   - The third quote is cut and closed with a full stop that is not in the source. The source reads "The CCM DEM dataset used in this research is not publicly available due to the use of proprietary data." followed by "The dataset can be requested for research purposes upon reasonable request."
   - The claim is in the present tense about the published maps, but the paper describes dataset v2.0.0 (2022-04-26). The current dataset is v3.1.1 (2026-03-05): "Horizontal resolution: 3 arc seconds (~90 m)", built with MERIT-DEM, MERIT-Hydro and EFAS v5.0, licence "Open Data Commons Open Database License v1.0". So "100 m" and "DEM not public" describe a superseded version. The README does not say whether v3 includes defences or which minimum upstream area it uses.
   - Safe to use: "the 2022 (v2.0.0) JRC maps were made with LISFLOOD-FP at 100 m, without local flood defences, for rivers above 500 km2".
7. `verified`. The Conclusions say "For the 1-in-100-year return period, the modelled maps can identify on average two-thirds of reference flood extent;" and continue "however they also largely overestimate flood-prone areas in many regions". This is for v2.0.0, validated against official maps in Spain, the Po basin, Norway, England and Hungary, not Romania. "Accuracy ceiling" is the researcher's reading, not the paper's: a result from a superseded continental run is a reference point, not an upper bound.
8. `verified` for the headline only. The quote is in the abstract (NHESS 24, 539, 15 Feb 2024), three villages in Vietnam. Limits:
   - 37 % and 62 % CSI appear in the text as scores for specific parcel comparisons, not clearly as a range across the three sites. "> 0.8 CSI" appears; "at peak for two sites" was not confirmed. Do not reuse the numbers without reading the paper.
   - The model is the "University of Bristol/Fathom global flood model", run by the authors. Only "a similar version of the model" is public, flood defences were not included, and "GFM MERIT data are available from Fathom for academic purposes".
9. `unsupported`. The source opens (Hawker et al., ERL 17, 024016, 3 Feb 2022). It supports that FABDEM removes buildings and forests from the Copernicus DEM and that tree and building artifacts "can act as dams that change overland flow pathways". It does not mention levees, and "bias-corrected" is not its wording. The statement that satellite DEMs cannot resolve levees has no source here.
10. `verified` for the GRDC access part only. The quote is the FAQ answer to "Is there an API to get GRDC discharge data automatically?", which starts "Unfortunately, not." The station ID, the PANGAEA series and its CC BY 3.0 licence are not on the cited page. Search snippets agree on GRDC 6742900 and PANGAEA monthly data 1921–1984, but I did not open those pages.
11. `verified`. The quote is on the JBA page. The page shows no publication date; 2023-10-05 comes from the URL. Vendor statement only.
12. `verified`. "Today, Flood Foresight has been deployed in over 20 countries and territories," is on the page, as are the four use cases. No pricing, no free or open access statement, Romania not mentioned. The date is inferred from the URL.
13. `verified` for this page only. The quote is there, and the page has no pricing, no free tier and no country list. Two corrections: the page is "Flood Foresight - Surface Water Flood Forecasting", not the main product page (it links to jbagr.com, which nobody opened), and the 30 m statement is on the page cited in claim 11, not on this one.
14. `verified`. The quote is on the page (NHESS 21, 1807, 14 Jun 2021), with the 300 m DEM and "The current early flood warning system offers a 120 h lead time". "Super Model" does not appear. The paper is about social vulnerability and describes the FFWC system in passing, so it is a secondary source for the model.
15. `verified`. The quote and "247 catchments across Bangladesh" are in the article (The Business Standard, 26 Oct 2025). News article, not a technical source.
16. `unreachable`. Access denied for me too, on the PDF and on the landing page.
17. `verified`. The quote is in the abstract (Earth Science Informatics, 13 Jan 2024). The abstract also says "comparable predictive capability of the HAND model to map flood inundation areas during extreme rainfall events" and names two 2D models, HEC-RAS 2D and SMS-SRH 2D. The rating curve was "developed from LIDAR DEM", so the result is for HAND on LiDAR terrain with a discharge and rating curve.
18. `verified`. The quote is in the abstract (GMD 18, 3387, 12 Jun 2025). The thing that outperforms is the Blackbird model, which pairs DHAND with a 1D steady-state solver; it "also outperforms a traditional HEC-RAS 1D model". One site (Grand River near Waldemar, Ontario), 2 m terrain, HEC-RAS 2D as the benchmark. "Plain HAND is a cheap, rough baseline" is the researcher's inference.
19. `verified` for the licence parts. The quote is in the README; the binaries are under the Deltares freeware licence ("Commercial use allowed, Research publishing allowed, no distribution, no modification"). The version is wrong: the README and the docs both show v2.5.0 ("Hautacam"), not v2.4.0.
20. `unreachable`. The cited PDF is over the fetch size limit. Checked separately on https://www.hec.usace.army.mil/software/hec-ras/download.aspx : 7.0.2 is the newest listed version, "Use is not restricted and individuals outside of USACE may use the program without charge.", Windows 10/11 64-bit with Linux for compute engines only. That page does not say "public domain", so the public-domain statement stays unconfirmed.
21. `verified`. The quote is in the README, with the "GPU and multicore solver introduced in ANUGA 4.0" and installation from conda-forge. The licence is not named on the page.
22. `verified`. Both statements are in the README ("Itzï requires GRASS GIS 8.5 or above."). "2.0" comes from the GitHub sidebar ("GPL-2.0 license"), not from the README.
23. `unreachable`. The EDF page returns 403 and the opentelemac.org presentation page returns 404. Nothing in this claim is confirmed.
24. `unreachable`. MDPI returns 403 on both URL forms and the conference PDF could not be read. Nothing in this claim is confirmed.
25. `verified`. Both quotes and all the details are on the page (5 m and 20 m versions, 1:50,000 contours, "The contours derive from the 1995 Romanian Topographic Map", last edited 3 July 2024, status June 2024). I could not read the OGL-ROU-1.0 licence text, so whether it allows use in a product is not confirmed.
26. `verified`. The sentence is verbatim in the abstract (arXiv:2606.08876v1, 7 Jun 2026). Zone A counties, the 0.5 m DTMs and the 1–2 m and 5 m statement are confirmed; the LAKI licence is not stated. The paper does not mention Galați, which shows only that this paper lists no coverage there. Single-author preprint.

### What the researcher missed
- **LISFLOOD-FP 8.3 exists** (13 Oct 2026), and the Zenodo licence field for 8.2 and 8.3 says GPL v2.0 only, against GPL v3 in the papers. https://zenodo.org/records/13121102/latest , https://zenodo.org/records/13121102
- **The JRC maps were superseded twice** since the cited paper: v3.0.0 (2024-03-08), v3.1.0 (2024-11-08), v3.1.1 (2026-03-05), about 90 m, MERIT-based, ODbL. v3.1.0 adds a layer of "spurious depth areas" where "Very high water depths may be caused by limitations in the hydraulic model". The validation in claim 7 was not repeated here for v3. https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/CEMS-EFAS/flood_hazard/README.txt , https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/Live/CEMS-EFAS/flood_hazard/CHANGELOG.txt
- **FABDEM is not free for a product.** Fathom: "This data is available under a commercial license or free for non-commercial use." Claim 8 presents FABDEM as the better DEM without saying this. https://www.fathom.global/insight/fabdem-download/
- **Flood Foresight has an independent evaluation**, and it is the paper in claim 16: Hooker, Bevington and Shelton (2023), "A multi-system comparison of forecast flooding extent using a scale-selective approach", Hydrology Research 54(10), 1115–1133. Search snippets say it compares Flood Foresight (30 m), GloFAS Rapid Flood Mapping (1,000 m) and the FFWC Super Model (300 m) for the July 2020 Jamuna flood against SAR-derived extent, and that the Super Model does best at short lead times. This is also where the name "Super Model" is used. I could not open it, so it is a lead, not a verified source. https://centaur.reading.ac.uk/113412
- **SFINCS is at v2.5.0.** https://github.com/Deltares/SFINCS
- **HEC-RAS has Linux compute engines** in 7.0.x and a separate "HEC-RAS 2025 Beta", so "Windows-first" is right for the interface only. https://www.hec.usace.army.mil/software/hec-ras/download.aspx
- **GRDC appears to list a second station upstream of Ceatal Izmail**, Lungoci (6742700), with a record from 1950 to 1970. Seen in a search snippet only; it would not help a model of recent floods. https://www.compositerunoff.sr.unh.edu/html/Polygons/P6742700.html
- **No independent source was given for the levee problem**, which the roadmap verdict leans on. Claim 9's paper does not cover it.

### Problems in "Relevance to LandHorizon"
The overall verdict (roadmap item, not buildable by 6 Dec) fits the constraints: the time budget, the rule that the team must be able to explain the method, and the value of a well-argued roadmap item. These points in the section are not backed by a verified claim, or go further than one:
- **"There is no free daily Siret/Prut discharge series."** Claim 10 only says none was found, and only its GRDC access part is verified. It should read "not found".
- **Terrain bullet.** It rests on claim 9 (unsupported for levees) and on claim 6 (superseded). The researcher labels claim 9 a lead, but the argument still uses it.
- **Licence bullet.** "GPL v3" for LISFLOOD-FP rests on claim 2, where the sources conflict (GPL v3 in the papers, GPL v2.0 only on Zenodo). Commercial use is allowed under either, so the practical point holds. "Older LISFLOOD-FP versions were described as non-commercial; do not use one" has no source: the Bristol page is undated, names no version and still carries that wording today. "HEC-RAS is free" is confirmed by the download page, not by claim 20's source.
- **HAND bullet.** Claims 17 and 18 test HAND with a discharge and a rating curve or Manning's equation on LiDAR-based terrain (2 m in claim 18). Our HAND is a 30 m GLO-30 index with no discharge. Those papers do not show that our HAND gives "comparable extent", and claim 18 says the simple method was vastly outperformed. The "terrain-based susceptibility screen" wording does fit the constraint that the product is a screening indicator, not a probability.
- **Reuse bullet.** "100 m" is the superseded version. The section also does not say that a 90–100 m grid is much coarser than a plot of under 1 ha to 5 ha, which the constraints require to be presented as describing the region, not the plot.
- **Flood Foresight bullet.** "Vendor-only evidence" is incomplete (see Hooker et al. above). "No free tier found" rests on two JBA Consulting pages; the product page at jbagr.com was not opened.
- **Romanian data bullet.** The OGL-ROU-1.0 terms were not read by the researcher or by me. The constraints ask for a check that the licence allows use in a product.
- **Pitch line.** "ANAR/INHGA gauge data and defence geometry that are not open" states as fact what the open questions list as "not found".
- **Compute bullet.** The Colab remark and the effort estimate are the researcher's own and are labelled as such. Neither can go into a synthesis as a finding.

### Untrusted content
No fetched page and nothing in this file contained instructions addressed to the reviewer.
