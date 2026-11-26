# Which EGMS product and level suits plot-level screening, and how to summarize motion for a plot with 0-1 cells (G1)
Date: 2026-11-12
Scope: Part A (what InSAR can and cannot say about a plot) kept short; Part B (Basic L2a / Calibrated L2b / Ortho L3, coverage, releases, access, licence, summarizing, trade-off). Out of bounds: velocity thresholds, accuracy numbers, non-EGMS data, own InSAR processing.

Method note: the research session was interrupted by a usage limit. Quotes below were returned by the fetch tool's page summarizer from the pages named; I could not re-open each page myself, so confidence is capped at medium. Several sources (Product User Manual, QGIS guideline, Explorer manual, ISPRS density paper PDF) were not readable (401 or binary PDF) and are listed under "not found".

## Claims

### Part A: what InSAR can and cannot say
1. **Claim:** InSAR measures displacement projected on the satellite line of sight (LOS), not true 3D motion.
   - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Algorithm_Theoretical_Basis_Document_v4.html
   - Quote: "InSAR displacement measurements are projected in the satellite's 'line-of-sight'"
   - Source date: ATBD v4 (exact date not captured; EGMS-D3-ALG-SC1-2.0-006 was dated 20/12/2021)
   - Source type: official docs
   - Confidence: medium

2. **Claim:** Measurement points exist mostly on stable reflectors; vegetated land has few, water has none.
   - Source: same ATBD, Section 3.4
   - Quote: "PS density depends heavily on terrain cover" ; "vegetated areas exhibit a low density of radar targets suitable for InSAR measurements" ; "No measurement points are identified over water and in general where radar reflectivity changes with time."
   - Source date: as above
   - Source type: official docs
   - Confidence: medium

3. **Claim:** Ploughed fields, changing vegetation and construction cause decorrelation (no points).
   - Source: same ATBD
   - Quote: "changing vegetation, ploughed fields, demolition/construction of buildings"
   - Source date: as above
   - Source type: official docs
   - Confidence: medium

4. **Claim:** Fast or abrupt motion cannot be tracked: phase aliases above about 14 mm between two Sentinel-1 acquisitions; abrupt, discontinuous or rapid displacements cause unwrapping problems.
   - Source: same ATBD
   - Quote: "(about 14mm for Sentinel-1) between two subsequent acquisitions" ; "Ground movements that cause unwrapping difficulties include abrupt, discontinuous, or rapid displacements."
   - Source date: as above
   - Source type: official docs
   - Confidence: medium

5. **Claim:** Steep terrain causes geometric distortion; ascending and descending geometries each cover slopes the other cannot. North-south motion is not measured per point.
   - Source: ATBD (above) and https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
   - Quote: "Geometric distortions are present in areas of significant topography" (ATBD) ; "Vertical, and east-west components are estimated thanks to a spatial interpolation of the information available." (Product Description, summarizer-returned)
   - Source date: ATBD v4; Product Description v3.0.1, 2025-08-07
   - Source type: official docs
   - Confidence: medium

6. **Claim:** Long-lasting flooding or burning reduces point density.
   - Source: https://land.copernicus.eu/en/faq/products/european-ground-motion-service/how-do-floods-and-wildfires-affect-egms-measurement-points
   - Quote: "may adversely affect the quality and density of measurement points"
   - Source date: not stated
   - Source type: official docs
   - Confidence: medium

### Part B.1: the three levels
7. **Claim:** Basic (L2a) is LOS displacement, per track, referenced to a virtual reference point, so only meaningful inside the processed area and not comparable across adjacent products.
   - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
   - Quote: "provides InSAR displacement data provided in the satellite line-of-sight." ; "It is not possible to compare deformations from adjacent areas belonging to different products of the same level."
   - Source date: 2025-08-07 (v3.0.1)
   - Source type: official docs
   - Confidence: medium

8. **Claim:** Calibrated (L2b) is still LOS per track but referenced to a GNSS-derived model (50 km grid, 3D velocities), which makes it absolute. Islands without GNSS are not referenced.
   - Source: same Product Description
   - Quote: "Calibrated products, containing absolute measurements, overcome the intrinsic limits of the Basic ones." ; "the reference model contains average velocities in 3D (east, north, up) on a 50-km grid."
   - Source date: 2025-08-07
   - Source type: official docs
   - Confidence: medium

9. **Claim:** Ortho (L3) gives two layers, purely vertical and purely east-west, on a 100 m grid, built from both ascending and descending Calibrated data; areas of strong relief have no Ortho values. Aimed at newcomers.
   - Source: same Product Description
   - Quote: "one of purely vertical displacements, the other of purely east-west displacements" ; "resampled to a 100 m grid to coincide with other Copernicus products." ; "ease of understanding to those new to InSAR"
   - Source date: 2025-08-07
   - Source type: official docs
   - Confidence: medium

10. **Claim:** Attributes. Basic/Calibrated points: mean_velocity, mean_velocity_std, acceleration, seasonality, temporal_coherence, rmse, amplitude_dispersion, incidence/track angles, LOS direction cosines, time series. Ortho: mean velocity, RMSE, acceleration, seasonality, time series.
    - Source: same Product Description (Table 5 and Ortho attributes)
    - Quote: "temporal_coherence, rmse, amplitude_dispersion" (Section 8)
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium for points; low-medium for the Ortho list (summarizer paraphrase, check PDF Section 5.2)

11. **Claim:** Formats. Basic and Calibrated are vector points, one zip per burst (CSV plus XML header). Ortho per tile has two GeoTIFFs (vertical and east-west mean velocity) plus CSV time series. Tiles are 100 x 100 km.
    - Source: same Product Description
    - Quote: "For each tile there are two Geotiff files containing the vertical mean velocity and the east-west mean velocity." ; "100 x 100 km tiles according to EEA recommendations."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium. The Ortho GeoTIFF is already a raster, so our "rasterize" step may be only mosaic and clip.

### Part B.2: density and Ortho cell construction
12. **Claim:** Ortho cell value = average of all points in the cell per geometry, then decomposed; cells need points in both geometries and cells below a "predefined number" are rejected (number not given).
    - Source: ATBD v4 Section 9 / 9.3, https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Algorithm_Theoretical_Basis_Document_v4.html
    - Quote: "All measurement points belonging to the same grid cell and to the same acquisition geometry are averaged" ; "Rejecting grid-cells with less than a predefined number of points will ensure the level of precision required" ; "at least 1 MP in each acquisition geometry"
    - Source date: ATBD v4
    - Source type: official docs
    - Confidence: medium (the two minimum-point statements are not fully consistent; numeric threshold not found)

13. **Claim:** Density targets exist only for urban and bare classes: 5,000 MP/km2 continuous urban, 1,000 for discontinuous urban and industrial, 100 for sparsely vegetated open space. No target for arable, pasture or forest is listed. Ortho density is just whatever L2b gives, downgraded to 100 m.
    - Source: Product Description v3, Section 4.1 Table 1 and Ortho attributes
    - Quote: "CLC18-1.1.1 'Continuous Urban Fabric': >= 5,000 MP/km2." ; "Dependent on the point density in L2b, downgraded to a 100 x 100 m resolution."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium (the absence of farmland rows is as reported by the summarizer)

14. **Claim:** Ortho nodata value: not specified in the Product Description; areas of high relief have no Ortho data ("In such areas, there are no EGMS _Ortho_ measurements.").
    - Source: Product Description v3
    - Quote: "In such areas, there are no EGMS _Ortho_ measurements."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium

15. **Claim:** A validation of point density per land-cover class exists (12 sites, Urban Atlas), but per-class figures could not be read.
    - Source: https://isprs-archives.copernicus.org/articles/XLVIII-4-W7-2023/247/2023/
    - Quote: "The study employs open land cover data to evaluate the density per class."
    - Source date: 2023-06
    - Source type: peer-reviewed (ISPRS Archives)
    - Confidence: low for any density number (none obtained)

### Part B.3: releases
16. **Claim:** Release history: baseline Feb 2015-Dec 2020; 1st update to Dec 2021; 2nd update Jan 2018-Dec 2022; 3rd update Jan 2019-Dec 2023; one delivery per year; five-year window from the 2nd update.
    - Source: Product Description v3
    - Quote: "EGMS is a one-delivery-per-year project." ; "a 5 full years nominal time range."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium

17. **Claim:** The 2020-2024 release was announced 2026-04-29; the Explorer keeps only the two latest releases; older ones are archived (request via helpdesk) and later move to CDSE.
    - Source: https://land.copernicus.eu/en/news/egms-annual-update-brings-new-data-improvements-to-egms-explorer
    - Quote: "covering the reference period 2020–2024"
    - Source date: 2026-04-29
    - Source type: official docs
    - Confidence: medium

18. **Claim:** The Explorer front page now lists a 2020-2025 release, so 2020-2025 is likely current (undated on the page). The CLMS FAQ still talks about the 2020-2024 update as upcoming, so it is stale.
    - Source: https://egms.land.copernicus.eu/
    - Quote: "2025 data now available." (heading "New update published")
    - Source date: page seen 2026-11
    - Source type: official docs
    - Confidence: medium

### Part B.4: access
19. **Claim:** The Explorer requires an EU Login to search or download. The team's belief about a login is correct for the Explorer route.
    - Source: https://egms.land.copernicus.eu/
    - Quote: "You must log in before performing a search."
    - Source date: seen 2026-11
    - Source type: official docs
    - Confidence: medium

20. **Claim:** "Cannot be scripted" is wrong. An official Jupyter notebook downloads EGMS through an API using a CLMS API token created once after login; the 2026 update adds a machine-to-machine interface; an Ortho WCS was announced.
    - Source: https://land.copernicus.eu/en/products/european-ground-motion-service/egms-basic ; https://github.com/copernicus-land/egms-api ; news page above
    - Quote: "A Jupyter Notebook allows downloading EGMS data through an API." ; "To use this notebook, you must obtain a CLMS API token from the Copernicus Land Monitoring Service website." ; "Users can search and download EGMS data through a machine-to-machine interface, offering a second access option."
    - Source date: 2026
    - Source type: official docs
    - Confidence: medium (last quote is the summarizer's wording; endpoints, rate limits and tile format not found)

21. **Claim:** CLMS machine-to-machine tokens: a logged-in user creates a service key, signs a JWT, exchanges it for a short-lived bearer token.
    - Source: https://land.copernicus.eu/en/how-to-guides/how-to-download-spatial-data/how-to-download-m2m
    - Quote: "A logged in-service user issues a service key in the portal."
    - Source date: not stated
    - Source type: official docs
    - Confidence: medium (page does not mention EGMS)

22. **Claim:** Third-party EGMStoolkit downloads, merges and clips EGMS data using a temporary token from any Explorer download link. Beta, whether login is needed to get the token is not stated.
    - Source: https://github.com/alexisInSAR/EGMStoolkit
    - Quote: "It can be found at the end of download links" ; "Any download links can be used, the user can use a random download link."
    - Source date: Version 0.3.0 Beta, Oct 2025
    - Source type: vendor (open-source project)
    - Confidence: medium

### Part B.5: licence
23. **Claim:** CLMS data policy: "full, open and free access"; attribution required when distributing; modifications must be stated; no implied EU endorsement; user owns IP in products they create.
    - Source: https://land.copernicus.eu/en/data-policy
    - Quote: "full, open and free access" ; "Generated using European Union's Copernicus Land Monitoring Service information;" ; "European Union's Copernicus Land Monitoring Service information;"
    - Source date: not stated
    - Source type: official docs
    - Confidence: medium. Use in a product and redistributing a derived raster look permitted with attribution and a modification note; the three numbered conditions were not read verbatim.

### Part B.6 and B.7
24. **Claim:** Published guidance for summarizing motion over a small area from sparse points or 100 m cells (nearest point, buffer, minimum count): not found. The Product Description Section 8 has no single-point warning; the PUM and QGIS guideline were unreadable.
    - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
    - Quote: "Some of the quality checks are available in the products download unit."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: low (absence of evidence)

25. **Claim (trade-off):** Basic and Calibrated points carry LOS geometry fields and are per track; Ortho needs points from both geometries in a cell, drops N-S, and is simpler and absolute. The sources do not rank them for small-plot screening.
    - Source: Product Description v3 (claims 7-12)
    - Quote: "ease of understanding to those new to InSAR" ; "Ascending and descending calibrated data are then averaged on to a common 100x100 m grid." (ATBD)
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: low-medium

## Relevance to LandHorizon
- **Product choice:** Skip Basic (not comparable across areas). Ortho is easiest to explain and fits one COG, but its GeoTIFFs already exist per tile, so our step is mosaic and clip rather than rasterize. Calibrated points are denser and would need per-track handling and a point-to-plot rule; heavier for the time budget.
- **Coverage honesty:** a 100 m cell is about 1 ha. Farmland, ploughed fields and water give few or no points and Ortho needs both geometries, so many Galati cells will be empty. Empty cells must be `unknown`, never "stable". A plot of 1 ha or less hits 0-1 cells: report the neighbourhood or nearest valid cell and say it describes the surroundings. No published rule was found, so our rule (distance, minimum count) is our own and must be fixed before testing.
- **Access and cost:** EU Login needed (confirmed), but scripting is possible via a CLMS API token (claim 20). Free. A one-off manual download still fits the schedule. Tile size 100 x 100 km; number of Galati tiles: not found (probably 1-2, unverified). Rasters stay out of git except samples.
- **Release:** latest is probably 2020-2025 (five-year window); only two releases remain in the Explorer, so store the release name in metadata.
- **Licence:** free with the attribution wording above plus a statement of modification. No cost.
- **Compute:** negligible (GDAL or rasterio mosaic and clip).

## Open questions
- Exact minimum point count per Ortho cell and the GeoTIFF nodata value: not found (ATBD 9.3 and PDF Section 6.3).
- Point density for farmland and forest, and anything Romania- or Galati-specific: not found; ISPRS 2023 PDF results unread.
- Tile IDs covering Galati, and whether the API serves Ortho GeoTIFFs: not found.
- Not read: Crosetto 2020 (Remote Sensing) and 2025 reviews, Cuervas-Mons 2024 (Applied Sciences, landslide limits), the Product User Manual.
- Projection (EPSG:3035 expected) and resampling to our grid: not checked.
- Out of scope: velocity classes and accuracy numbers belong to the other researcher.

## Review
Reviewer: independent verifier, 2026-11-12. I did not write this file.

**Method.** I opened every cited URL again with WebFetch. WebFetch returns text through a page summarizer, and I had no raw-text access, so these quote checks have the same limit the researcher reported. The ISPRS PDF could not be rendered. Where a pass over a truncated page section said "NOT PRESENT", I did not count that as evidence of absence: the first ATBD pass missed the 14 mm figure, which is in Section 4.7.

**Verdict rule.** A claim is `verified` when its quote carries the core of the claim and I confirmed any extra parts in a cited source. Those parts are quoted in the note so the synthesis can use them. A claim is `unsupported` when a substantive part has no support in any cited source. Changes of case and trimmed quotes are noted but are not counted as misquotes.

**Source dates.**
- Product Description (PD): published 2025-08-07. The document history lists v3.0 as 06/08/2025. The current change-log entry is 3.0.2, dated 2026-10-29. The researcher's "v3.0.1, 2025-08-07" mixes two entries, because 3.0.1 is dated 2026-06-03 in the change log.
- ATBD: v4.0, 07/08/2025, with change log 4.0.2 dated 2026-10-29. The date in claim 1, "EGMS-D3-ALG-SC1-2.0-006, 20/12/2021", was not confirmed.
- These dates were extracted by the tool, and the ATBD history table it returned has dates out of order.

### Verdicts
1. `verified`: ATBD Section 1.3 glossary, quote present.
2. `verified`: ATBD Section 3.4, all three quotes present.
3. `verified`: ATBD Section 3.2 (noise term), quote present.
4. `verified`: ATBD Section 4.7. Motion is measured correctly only below lambda/4 ("about 14mm for Sentinel-1"), and larger motion is "aliased". The unwrapping quote is in Section 3.2.
5. `verified`, with a quote fix needed. Both quotes are present, but the source has "Therefore, vertical, and east-west..." in lower case. The other parts of the claim are in the cited sources but not in the quotes:
   - ATBD Section 2.6: "areas affected by foreshortening or layover in one acquisition geometry will correspond" (to slopes well sampled by the other geometry).
   - PD Section 2.3: "north-south displacement components are not available for any MP, since they are estimated from GNSS data."
6. `verified`. The FAQ is explicit about prolonged flooding ("prolonged water coverage ... over days or weeks"). For wildfires it says "substantial surface changes in burnt areas", not long-lasting burning. The page has no date.
7. `verified`: both quotes present in the PD. The PD also says Basic products are "meaningful just considering the processed area".
8. `verified`: both quotes present. The islands part is in PD Section 2.2, not in the quote: "Some isolated islands may not have GNSS data available."
9. `verified`: the quotes are present, trimmed. Two parts are confirmed elsewhere in the PD:
   - Section 2.3: "To make the Ortho product, both ascending and descending geometry Calibrated products are needed."
   - Relief: "...(layover, foreshortening and shadow) prevent 100% coverage. In such areas, there are no EGMS Ortho measurements."
10. `verified`. The quote is from Section 8, not from Table 5. I confirmed the field lists in PD Table 5 (Section 5.1, Basic and Calibrated) and in Table 6 (Ortho: rmse, mean_velocity(_std), acceleration(_std), seasonality(_std), Time-series).
11. `verified`: both quotes present. The CSV time series is confirmed in PD Section 4.3: "Associated with each tile are also two CSV files, containing the time-series".
12. `verified`: ATBD Section 9 and Section 9.3, all three quotes present. Only "at least 1 MP in each acquisition geometry" is numeric.
13. `verified`. PD Table 1 has only three density rows: CLC 1.1.1 (>= 5,000), 1.1.2 and 1.2 (>= 1,000), and 3.3 (>= 100 MP/km2). It has no farmland or forest row.
14. `verified`: the PD does not mention a nodata value, and the relief sentence is present.
15. `unsupported`. The quote is present but cut mid-sentence, since the source continues "...per class and proposes statistical parameters". The page gives 12 sites, rural and urban, dated 22 Jun 2023, authors Vradi, Sala, Solari and Balasis-Levinsen. It says only "open land cover data" and does not name Urban Atlas, and the PDF could not be read to check. The source type "peer-reviewed" is not confirmed, because the page states no review process for this ISPRS Archives paper.
16. `verified`: the release ranges match the PD (baseline 02/2015-12/2020, 1st update 02/2015-12/2021, 2nd 01/2018-12/2022, 3rd 01/2019-12/2023). Both quotes are present, trimmed.
17. `verified`: news page dated 29 April 2026. It confirms the 2020-2024 release, that the Explorer keeps the two latest releases, the Helpdesk archive, and the move to CDSE "later in 2026".
18. `unsupported`. The Explorer part holds: "New update published" / "2025 data now available." and "Release: 2020-2024 2020-2025". The sentence about the CLMS FAQ being stale cites no URL, so I could not check it. A search found no announcement of a 2020-2025 release.
19. `verified`: "You are not logged in. You must log in before performing a search."
20. `misquoted`. The first two quotes are present (egms-basic page and the egms-api README). The third is not in the source. The news page says: "An API now enables users to search and download the EGMS data through a machine-to-machine interface". The Ortho WCS is confirmed ("will be released in the coming weeks"). The egms-api README does not say which products (Basic, Calibrated or Ortho) the API serves.
21. `verified`: the quote is present, and the service key, signed JWT and short-lived bearer token flow matches the page. The page does not mention EGMS and has no date.
22. `verified`: both quotes are present. The page shows v0.3.0 Beta, Oct 2025, "UNDER DEVELOPMENT", GPL-3.0. Its only example uses release `2018_2022`, and support for newer releases is not stated. It is better described as an academic open-source tool than as a vendor.
23. `verified`: all quotes present. The three conditions as returned:
   - (1) "users shall inform the public of the source of these products and services"
   - (2) for modified products, "the user shall clearly state this"
   - (3) "Users shall make sure not to convey the impression to the public" (of EU endorsement)

   IP: "the user has all intellectual property rights to the products he/she has created". The page lists "commercial" among the publication types and has no non-commercial restriction.
24. `verified`, as an absence claim for the PD only. The quote is present, and my own pass found no single-point or minimum-count guidance in the PD. See the missed FAQ below, which gives related guidance.
25. `verified`: both quotes present. The ATBD has "Ascending and descending Calibrated data..." with a capital C, and that quote comes from the ATBD (Section 9.3), not the PD that the claim cites as its source.

**Tally:** 22 verified, 2 unsupported, 1 misquoted, 0 unreachable.

### What the researcher missed
- **The documents describe older releases.** PD v3 and ATBD v4 describe releases only up to 2019-2023. The 2020-2024 release added "an enhanced quality-control strategy", with "More rigorous and robust checks" "particularly for the Ortho product". The Ortho cell rules for the current release may therefore differ from claims 9 and 12-14. https://land.copernicus.eu/en/news/egms-annual-update-brings-new-data-improvements-to-egms-explorer
- **EGMS limitations FAQ.**
  - Coverage "is not continuous".
  - "the actual x,y location of the point is known only to a few metres".
  - The data come from a 20 m x 5 m ground cell, and the effective resolution "may not be appropriate for some applications", such as "reliably mapping the motion of an individual, small house".

  This directly supports reporting surroundings, not the plot. https://land.copernicus.eu/api/en/faq/products/european-ground-motion-service/where-are-the-main-limitations-of-egms-data
- **Validation status.** Official validation reports exist for the 2015-2021 and 2019-2023 datasets. The 2019-2023 report was too large to fetch, so its land-cover density figures are not read. The egms-basic page lists validated datasets only up to 2018-2022 and 2019-2023, and I found no validation of the release now shown in the Explorer. https://land.copernicus.eu/en/technical-library/validation-report-2019-2023-dataset/@@download/file ; https://land.copernicus.eu/en/products/european-ground-motion-service/egms-basic
- **CDSE migration inside the project window.** The egms-basic page says data move to CDSE between Q4 2026 and Q1 2027, "where only data tiles can be downloaded". CDSE expects the whole CLMS portfolio by end of 2026 (https://dataspace.copernicus.eu/node/3136, which does not mention EGMS). The access route may change before 11 Dec. https://land.copernicus.eu/en/products/european-ground-motion-service/egms-basic
- **Open questions that are now answered.**
  - Ortho uses ETRS89-LAEA, EPSG:3035 (PD Table 3, Section 4.3).
  - Each Ortho tile has two CSV time-series files (PD Section 4.3).
  - The egms-api repo is EUPL-1.2 and states neither the products it serves nor rate limits.

### Problems in "Relevance to LandHorizon"
- **"Calibrated points are denser"** is not backed by any claim in this file. Remove it or source it.
- **"probably 1-2"** Galați tiles is a guess. The README says to write "not found".
- **The scripting route** rests on claim 20, which is partly misquoted. It still needs a one-time manual EU Login to create the token. Whether the API serves Ortho was not found, and the route may change with the CDSE move. With the data test on 15 Nov, the one-off manual Explorer download is the safer plan, and API scripting should be treated as unconfirmed.
- **Release choice.** "Latest is probably 2020-2025" rests on claim 18 (`unsupported` as written, though the Explorer part holds). The documented Ortho rules predate the 2020-2024 QC change, so do not apply claims 12-14 to the current release without checking.
- **"Store the release name in metadata."** If this means a new field in the API response, it changes the evidence contract and needs the lead's review (constraints, Architecture). Storing it in COG metadata only does not.
- **Compute.** `rasterio` is already in `pyproject.toml`, so the mosaic-and-clip step needs no new dependency. This is consistent with the constraints.
- **Coverage.** No source here confirms that Galați has Ortho coverage, meaning both geometries are present over farmland. Until it is checked, a missing cell must stay `unknown`, which the section already says.
