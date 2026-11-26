# Ground motion: synthesis

Date: 2026-11-12. Written by the research coordinator from the three reviewed findings files in this folder. Nothing here is a decision; decisions live in [architecture.md](../../architecture.md). What to do about it is in [RECOMMENDATIONS.md](../RECOMMENDATIONS.md).

| ID | File | Verdicts |
|---|---|---|
| G1 | [egms-products.md](egms-products.md) | 22 verified, 2 unsupported, 1 misquoted |
| G2 | [thresholds-uncertainty.md](thresholds-uncertainty.md) | 12 verified, 2 unsupported, 1 misquoted, 1 unreachable |
| G3 | [other-data-competitor.md](other-data-competitor.md) | 9 verified, 3 unsupported, 1 misquoted, 3 unreachable |

## How to read the evidence tags
- **[G1-9]** = claim 9 in file G1, marked `verified` by its reviewer. Only these carry a conclusion.
- **(R)** = something the reviewer found and opened while checking. Nobody checked the reviewer, so it is weaker than a verified claim.
- **not found** = searched for and not found, which is not proof of absence.
- **Limit of every verdict:** pages were read through a fetch tool that summarises. The EGMS validation reports and several PDFs could not be read by anyone.
- **No follow-up round was run.** Open gaps are listed at the end.

## Bottom line
1. **EGMS Ortho is the right level for us.** It is the only level that is absolute, comparable across areas and already on a 100 m grid [G1-7, G1-8, G1-9]. The planned choice holds.
2. **It describes the surroundings of a plot, not the plot.** EGMS's own FAQ says point positions are known only "to a few metres" and the data may not suit "an individual, small house" (R). Farmland has few or no measurement points [G1-2, G1-3, G2-10], so many Galați cells will be empty, and empty must be `unknown`.
3. **No velocity threshold has a verified source for EGMS.** Not 2 mm/year, not 5 mm/year. The only citable 5 mm/year is a 2013 landslide-activity threshold on older data, measured along the slope [G2-1]. No verified source links velocity to damage.
4. **No published rule exists for summarizing a small plot** (nearest cell, buffer, minimum count) [G1-24]. Whatever we pick is our own rule and must be written down before the data test. The competitor uses the median of 3×3 cells around the address [G3-12] and shows a signed number without classes [G3-13].
5. **The documentation describes older releases.** The product description and the algorithm document cover releases up to 2019–2023. The 2020–2024 release added stricter checks "particularly for the Ortho product" (R). No validation report covers the release we would download (R).
6. **Other ground data (landslide susceptibility, soil, seismic) is regional context or roadmap.** ELSUS says itself that it "should not be used to deduce local information" [G3-2], and its terms forbid passing the data to third parties [G3-3].

## 1. What InSAR can and cannot say about a plot
- **It measures motion along the satellite's line of sight,** not true 3D motion [G1-1]. North-south motion is not measured for any point [G2-12, G1-5].
- **Points exist where the radar signal is stable over time.** Density "depends heavily on terrain cover"; vegetated areas have few points and water has none [G1-2]. Ploughed fields and changing vegetation break the signal [G1-3]. Coverage "is not continuous", because vegetation decorrelates between images [G2-10].
- **Fast or abrupt motion is missed or wrong.** Motion above about 14 mm between two Sentinel-1 images aliases [G1-4]. With long snow cover, non-linear motion is ambiguous at about ±28 mm/year [G2-14].
- **Long flooding reduces point quality and density** [G1-6]. That matters for a floodplain pilot.
- **Density targets exist only for urban and bare classes** (5,000, 1,000 and 100 points per km²). There is no target for arable land, pasture or forest [G1-13]. Measured density on farmland, and anything specific to Romania: not found.

## 2. Which product
| Level | What it is | Fit for us |
|---|---|---|
| Basic (L2a) | Line-of-sight, per track, relative to a local reference point. "It is not possible to compare deformations from adjacent areas" [G1-7, G2-8] | No |
| Calibrated (L2b) | Line-of-sight, per track, tied to a GNSS model on a 50 km grid, so absolute [G1-8] | Roadmap: vector points per burst, needs a point-to-plot rule and per-track handling |
| **Ortho (L3)** | Two layers, "purely vertical" and "purely east-west", on a 100 m grid, built from ascending and descending Calibrated data; aimed at people "new to InSAR" [G1-9] | **Yes** |

- **How an Ortho cell is made:** all points in a cell are averaged per viewing geometry, then decomposed. A cell needs at least one point in each geometry, and cells with fewer than "a predefined number of points" are rejected; the number is not published [G1-12, G2-11]. The nodata value is not documented [G1-14].
- **Accuracy depends on the GNSS model** used for calibration, which in turn depends on station density [G2-7].
- **Format:** per 100 × 100 km tile, two GeoTIFFs (vertical and east-west mean velocity) plus CSV time series [G1-11]. The projection is ETRS89-LAEA, EPSG:3035 (R).
- **Attributes per cell:** `mean_velocity`, `mean_velocity_std`, `rmse`, acceleration and seasonality [G1-10, G2-13]. There is **no temporal coherence and no point count** in Ortho (R, product description Table 6).
- **Consequence for the pipeline:** the velocity rasters already exist, so the step is mosaic, reproject and clip. The uncertainty fields (`mean_velocity_std`, `rmse`) are listed as cell attributes, and the GeoTIFFs are described as holding mean velocity only. Whether the uncertainty has to be rasterized from the CSV is an inference to confirm in the 15 Nov data test.
- **"Calibrated is denser"** in the G1 relevance section has no source. Don't repeat it.

## 3. Releases, access and licence
- **Releases:** one delivery a year, five-year window [G1-16]. The 2020–2024 release was announced on 29 April 2026. The Explorer keeps the two latest releases, and older ones go to an archive [G1-17]. The Explorer page also lists "2020-2025" (R, from the part of claim G1-18 the reviewer confirmed); no announcement of that release was found.
- **The documents lag the data (R).** The 2020–2024 release brought "an enhanced quality-control strategy" with "more rigorous and robust checks ... particularly for the Ortho product". The cell rules in section 2 come from documents written for releases up to 2019–2023.
- **Validation (R):** official reports exist for the 2015–2021 and 2019–2023 datasets (too large for the fetch tool, not read). None was found for the current release.
- **Access:**
  - The Explorer needs an EU Login to search or download [G1-19].
  - An official notebook downloads EGMS "through an API" with a token created once after login [first two quotes of G1-20, confirmed by the reviewer]. The news item says "An API now enables users to search and download the EGMS data through a machine-to-machine interface" (R). **No source says the API serves Ortho.**
  - A third-party toolkit exists (beta, last example uses the 2018–2022 release) [G1-22].
  - EGMS data move to the Copernicus Data Space between Q4 2026 and Q1 2027 (R), so the route may change before 11 Dec.
- **So "EGMS can't be scripted" in the constraints is out of date in principle,** but unconfirmed for Ortho. A one-off manual download is the safe plan for the data test.
- **Licence:** Copernicus Land Monitoring Service data are "full, open and free". Conditions: name the source, state modifications, don't imply EU endorsement. The user owns what they create, and commercial publication is listed [G1-23]. Attribution wording: "Generated using European Union's Copernicus Land Monitoring Service information".
- **Security note (unreviewed):** the G1 researcher reported a `token.jwt` file listed in the public `copernicus-land/egms-api` repository. Don't use it; create your own token.

## 4. Thresholds and precision
| Figure | Source and meaning | Usable as |
|---|---|---|
| 0.7 mm/year (1 σ) | EGMS specification for mean-velocity standard deviation; for Basic and Calibrated it applies to points with coherence above 0.7 [G2-4]. A requirement, not a measured result | The product's stated precision |
| "Most differences below 2 mm/year" | Comparison with GNSS and corner reflectors for the first EGMS product (2015–2021), at sites with significant deformation [G2-5]. That product is now archived (R) | Context only. Not a noise floor for a rural plot |
| ±5 mm/year | Cigna et al. 2013: a landslide activity threshold from the precision of ERS and RADARSAT data projected on local slopes [G2-1] | Not an EGMS threshold. Cite only with that description |
| 16 mm/year | Boundary between "extremely slow" and "very slow" landslides, reduced by about 20 % in the same paper [G2-2] | A landslide intensity class, not for plots |

- **A multiple of the standard deviation as the "active" threshold** (the ADAtools approach): its source was `unreachable` (claim G2-3). No verified backing and no confirmed multiple.
- **Unverified lead:** Palama et al. (JISDM 2025) may give an EGMS-specific 5 mm/year threshold justified by about 2 mm/year noise. Seen in a search snippet only (R). If it holds, it is the first source for both of the team's numbers.
- **Contested (R):** a 2026 paper concludes InSAR is unreliable below 5 mm/year in vegetated coastal settings (US, not EGMS); a peer-reviewed comment disputes it. Relevant because our plots are vegetated farmland.
- **Velocity and damage:** no verified source (claim G2-15 `unsupported`). The product must not say or imply that a velocity means damage.
- **National services:** Norway's service shows velocity with a legend the user can change and no fixed classes [G2-16]. Class schemes of other countries: not found.

## 5. Wording uncertainty and `unknown`
- **Absence of points is not stability.** Where vegetation decorrelates, "no reliable data can be extracted" [G2-10].
- **A lone value is weak.** EGMS's FAQ says the data are not appropriate "to the analysis of individual buildings, unless they are large enough to cover the ambiguity", and advises reading clusters of points (R; claim G2-9 cut that qualifier and was marked `misquoted`). **If we quote the FAQ, quote the full sentence.**
- **Geolocation:** tolerances of about ±8 m north, ±12 m east and ±8 m vertical (R).
- **The label proposed in G2 can't be built from Ortho as written,** because it needs temporal coherence. Ortho offers `mean_velocity_std` and `rmse` only (R).

## 6. Other data and the competitor
**Landslide susceptibility and context**
- **ELSUS v2:** 200 m grid, classes 1 to 5, GeoTIFF [G3-1]; built from slope, shallow lithology and land cover only [G3-4].
  - "To be viewed at scales up to 1:200,000" and "should not be used to deduce local information" [G3-2].
  - Terms: registration, any purpose "including commercial gain", but "under NO CIRCUMSTANCES are these data passed to third parties" [G3-3]. A COG served through our API plausibly passes the data on, so it most likely fails the open-data rule until ESDAC says otherwise in writing.
  - A confidence map exists (R).
- **NASA:** LHASA 2 is a daily landslide nowcast at about 1 km, not a susceptibility map (R). A static susceptibility GeoTIFF exists; its resolution and licence are unchecked (R).
- **Romanian county landslide maps (HG 447/2003):** all three claims were `unreachable`, so nothing about their scale or availability is established. A 2024 government decision funds counties to make or update them (R); Galați is not named.
- **SoilGrids:** 250 m, CC BY 4.0 [G3-10]. Soil context, not instability.
- **Slope from our 30 m DEM:** no published threshold for this terrain was found. Seismic hazard: nothing established.
- **Scope:** landslide susceptibility is a different hazard from ground motion, so under the constraints it is out of scope after the 22 Nov gate.

**Imoreview** (vendor pages, November 2026)
- **Ground motion:** EGMS Ortho vertical, 2020–2024, "the median of the available values in a neighbourhood of 3 × 3 cells of 100 m around the address cell" [G3-12]. A signed mm/year number, no classes or colours, with the statement that it is not a geotechnical survey [G3-13].
- **Flood:** the address point against RO-FLOODS [G3-14].
- **Missing data:** a section is left out, and the sources page says a missing section means no verified data [G3-15].
- **Unit and price (R):** building and address based ("728,500 buildings"). Reading is free without an account, and four per-address products are sold at 19, 29, 79 and 179 lei. Claim G3-16 said only one was paid and was marked `misquoted`.
- **What we can honestly say is different:** our unit is a drawn plot of any size; our `unknown` is an explicit status, theirs is an omitted section; our flood layer is observed history, theirs is the official modelled map. We use the same ground data at the same resolution, so there is no advantage in the ground number itself.

## What could not be used
- **G1:** claims 15 (density paper, PDF unread), 18 (2020–2025 as current release; the FAQ part has no source), 20 (third quote altered).
- **G2:** claims 3 (`unreachable`: ADAtools threshold), 6 (wrong dataset years), 9 (quote cut), 15 (no source: damage link).
- **G3:** claims 5 and 6 (NASA products mixed up), 7–9 (`unreachable`: HG 447/2003), 11 (lithology statement not in the source), 16 (Imoreview pricing).

## Where sources disagree
- **Scripting:** the constraints say EGMS "can't be scripted"; EGMS announced an API in April 2026. Unresolved for Ortho.
- **Current release:** the April 2026 news and the FAQ say 2020–2024; the Explorer front page also lists 2020–2025 (R).
- **Reliability below 5 mm/year on vegetated land:** disputed between two 2026 papers (R).
- **Imoreview pricing:** the researcher read one paid product, the reviewer found four on the terms page.

## Open after this round (no follow-up was run)
- Palama et al. 2025: is there a sourced 5 mm/year EGMS threshold?
- What changed in the 2020–2024 Ortho quality control, and the minimum point count per cell.
- Does the API serve Ortho? Which tiles cover Galați, and how many cells have values on farmland? (the 15 Nov data test answers the last two)
- The validation report for 2019–2023, and whether one exists for the current release.
- HG 447/2003 text and whether a Galați county landslide map exists in digital form.
- ESDAC's answer on derived products from ELSUS.

## Follow-up round, 23 Nov 2026
One file, reviewed by a fresh reviewer: FU4 [egms-ortho-2020-2024.md](egms-ortho-2020-2024.md). `[FU4-1]` is claim 1 of FU4, marked verified.

- **No citable 5 mm/year threshold for Ortho.** Palamà et al. (JISDM 2025) [FU4-5] use 5 mm/year inside the ADAfinder tool to drop points considered stable before detecting active deformation areas [FU4-6]. They justify it with an average noise of "about 2 mm/year" for EGMS **Basic** [FU4-7], with no derivation, and their input is Basic only [FU4-8]. It is a detection filter for one product level, not a stability or damage threshold for a plot. **Decision 5's "no classes" stands,** and our 2 mm/year noise floor is sourced for Basic only, not Ortho. Claim 9 (another ±5 mm/year paper) cites no source: a lead only.
- **What changed in Ortho for 2020–2024 is still unknown.** The release added stricter quality control, "particularly for the Ortho product", without saying which checks [FU4-1]. The cell rule, nodata value and validation figures for this release are not found (FU4-4, no source). (R): the reviewer read the 2020–2024 patch note (28 May 2026). It lists post-release fixes, not the cell rule, and names a 2020–2024 Data Format Specification (5 May 2026) nobody has read.
- **Three practical points for the ground team (R, from the reviewer):**
  1. Patched tiles end in `_2`, so Ortho copies downloaded before 28 May 2026 may be out of date. Check the file names. The reviewer's reading that Galați was not patched is its own calculation, unsourced.
  2. EGMS moves to CDSE between Q4 2026 and Q1 2027, overlapping our final weeks: keep the downloaded tiles.
  3. The release adds a machine-to-machine API [FU4-2], and the Ortho page links an official API notebook (`copernicus-land/egms-api`) that uses a CLMS token. "EGMS can't be scripted" is therefore partly wrong; whether the API serves Ortho for 2020–2024 is unconfirmed. Never use the `token.jwt` published in that repository.
- **Effect on plots (FU4's inference):** stricter checks can only remove cells, so more plots may be `unknown` under the share rule. Count the cells in the 2020–2024 tiles over Galați to know.
- **Rejected from FU4's relevance section:** its suggested limits wording sets a plot-summary rule, which decision 5 already fixed. Keep decision 5's three sentences.
