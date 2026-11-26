# What changed in EGMS Ortho for the 2020–2024 release, and does any citable source support a velocity threshold (5 mm/year) or noise floor (2 mm/year) for EGMS?
Date: 2026-11-23
Scope: In: 2020–2024 release changes for Ortho, Ortho availability and API, the Palamà et al. (JISDM 2025) paper, other EGMS stable/moving thresholds. Out: landslide susceptibility maps, other InSAR products, the plot-summary rule, competitor products. Tool limit: my fetcher could not decode PDFs directly. The Palamà text below came through a text-extraction proxy (r.jina.ai) and a summarising model, so each quote is a fragment of 125 characters or fewer that the extractor returned. A reviewer should check them against the PDF.

## Claims
1. **Claim:** The 2020–2024 EGMS release keeps the processing chain and adds stricter quality control, "particularly for the Ortho product". The news item does not say which checks changed.
   - Source: https://land.copernicus.eu/en/news/egms-annual-update-brings-new-data-improvements-to-egms-explorer
   - Quote: "More rigorous and robust checks— particularly for the Ortho product—should provide users with greater confidence"
   - Source date: 2026-04-29
   - Source type: official docs (Copernicus Land news item)
   - Confidence: high (the page was opened twice; it gives no detail on the checks)

2. **Claim:** The release adds a machine-to-machine API for searching and downloading EGMS data. A WCS for Ortho was announced as upcoming. The page does not say the API serves Ortho.
   - Source: https://land.copernicus.eu/en/news/egms-annual-update-brings-new-data-improvements-to-egms-explorer
   - Quote: "An API now enables users to search and download the EGMS data through a machine-to-machine interface,"
   - Source date: 2026-04-29
   - Source type: official docs
   - Confidence: medium (the page is not explicit about Ortho in the API)
   - Second quote, same page: "Looking ahead, a Web Coverage Service (WCS) for the Ortho product will be released in the coming weeks."

3. **Claim:** A "Product Patch Note" for the 2020–2024 dataset exists on the Copernicus Land technical library (PDF dated 28 May 2026, 11 pages). I could not read its text: the fetcher returned compressed binary, and the proxy returned a 500 error. Its content on Ortho rules, nodata and tiles is **not found**.
   - Source: https://land.copernicus.eu/en/technical-library/patch-note-2020-2024-dataset-european-ground-motion-service/@@download/file
   - Quote: "PRODUCT PATCH NOTE"
   - Source date: 2026-05-28 (PDF creation metadata)
   - Source type: official docs
   - Confidence: low (only the title and metadata were read)

4. **Claim:** The Ortho cell rule (points in both geometries, minimum point count, nodata value) for 2020–2024, a 2020–2024 validation report, and the Ortho tile format and projection for that release are **not found** in anything I could open. A web search surfaced a validation report only up to 2019–2023 (v3.0, 2025-06-02) and an End User Interface Manual v3.0 (2023-11-16) that predates the release. I did not open either document. Earlier research (v3 and v4 documents) stays the baseline.
   - Source: none openable
   - Quote: not found
   - Source date: n/a
   - Source type: n/a
   - Confidence: n/a

5. **Claim:** Palamà et al. (JISDM 2025) is "Wide-Area Supervised Classification of Ground Deformation Phenomena from European Ground Motion Service Products". The authors are Palamà, Barra, Cuevas-González, Pawłuszek-Filipiak, Navarro, Monserrat and Crosetto. It was published on 2025-03-28 in the KIT repository (DOI 10.5445/IR/1000180535).
   - Source: https://publikationen.bibliothek.kit.edu/1000180535
   - Quote: "Wide-Area Supervised Classification of Ground Deformation Phenomena from European Ground Motion Service Products"
   - Source date: 2025-03-28
   - Source type: conference proceedings (open-access PDF: https://jisdm2025.gik.kit.edu/downloads/JISDM2025_Palama_et_al.pdf)
   - Confidence: high

6. **Claim:** The paper does use 5 mm/year as a threshold. It is applied inside the ADAfinder detector, which removes points considered stable before grouping the rest into Active Deformation Areas (ADAs). The purpose is detection of active deformation areas as an input to a landslide, subsidence and slope-deformation classifier. It is not a threshold for judging land as safe or stable.
   - Source: https://jisdm2025.gik.kit.edu/downloads/JISDM2025_Palama_et_al.pdf (read via text proxy)
   - Quote: "In this work we set the value of this threshold at 5 mm/year, considering that the average noise level"
   - Source date: 2025-03 (proceedings of JISDM, 7–9 April 2025)
   - Source type: conference proceedings
   - Confidence: medium (the quote is a fragment returned by an extractor; the PDF was not opened directly)

7. **Claim:** The paper justifies 5 mm/year by an average noise level of about 2 mm/year for the EGMS **Basic** product velocities. So the 2 mm/year figure is the paper's own estimate of the average noise of the Basic product, not an official EGMS spec.
   - Source: https://jisdm2025.gik.kit.edu/downloads/JISDM2025_Palama_et_al.pdf (via text proxy)
   - Quote: "the average noise level for the velocity values of the EGMS Basic product is about 2 mm/year"
   - Source date: 2025-03
   - Source type: conference proceedings
   - Confidence: medium (same extraction caveat; I could not see how the 2 mm/year was derived or cited)

8. **Claim:** The paper's input is the EGMS Basic product (ascending and descending, per-geometry line-of-sight velocities). Calibrated and Ortho are not mentioned in the extracted text. So the threshold applies to Basic, not to Ortho.
   - Source: https://jisdm2025.gik.kit.edu/downloads/JISDM2025_Palama_et_al.pdf (via text proxy)
   - Quote: "The main input of the GMC consists of the EGMS Basic Product data, derived from Sentinel-1 data,"
   - Source date: 2025-03
   - Source type: conference proceedings
   - Confidence: medium

9. **Claim:** Another published EGMS work classes points as active or non-active using a ±5 mm/year displacement-rate threshold. It justifies the figure as exceeding noise by two standard deviations in the 1339 bursts it analysed. It is the **search-engine snippet only**: I did not open the source, so it is not cited as evidence here. Lead only.
   - Source: not opened (search result for ResearchGate record 403674126, "Beyond the European Ground Motion Service: Identification and Classification of Unstable Areas at the National Level"; ResearchGate returned HTTP 403)
   - Quote: not found (not opened)
   - Source date: not found
   - Source type: not found
   - Confidence: low

## Relevance to LandHorizon
- **Plots getting cells in 2020–2024:** not found. The patch note and updated Product Description would say whether the Ortho cell rule or nodata changed, and I could not read them. The news item says only that Ortho checks became "more rigorous", which could mean fewer or more cells than 2019–2023. Inference (not sourced): treat the cell count as unknown until we count Ortho cells ourselves over Galați after the download. A stricter filter can only remove cells, so it can push more plots to `unknown` under the "fewer cells than half the hectares" rule.
- **Is a threshold citable:** only Palamà et al. gives one, with a stated purpose. 5 mm/year is a detection threshold for flagging Active Deformation Areas from EGMS **Basic** points, and about 2 mm/year is that paper's average noise estimate for Basic. It is not an EGMS threshold, and it is not for Ortho (100 m cells, vertical and east-west). It does not fit a land buyer's screening report: it detects moving areas for later classification, and it does not certify a plot as stable. Using it for Ortho would borrow a number from another product level and purpose.
- **Suggested limits wording (inference):** "Ground motion is the median velocity of EGMS Ortho cells (100 m) whose centre lies inside the plot. We show the number as measured and do not classify it. A published study (Palamà et al., 2025) used 5 mm/year to separate moving from stable points in the EGMS Basic product, with an average noise of about 2 mm/year. That figure is not an official EGMS threshold and was not set for the Ortho product used here. A value near zero does not prove the plot is stable, and a plot with too few cells is shown as unknown." Mark the Palamà sentence as sourced and the rest as our inference.
- **Data access, licence, cost, compute:** an API now exists per the news item (sourced), but whether it serves Ortho, how it authenticates, and its terms are not found. The EGMS login remains manual per the project notes. Ortho WCS was only announced ("coming weeks" as of 2026-04-29). Whether it has shipped is not found. Format and projection of the 2020–2024 Ortho tiles are not found. Cost is zero for download; compute is unchanged.
- **Coverage of Galați:** not found for 2020–2024.

## Open questions
- Read the patch note PDF (11 pages, 2026-05-28) and the Product User Manual dated 10/12/2025 and Basis Document dated 05/05/2026 named in a search snippet. Someone with a PDF reader should extract the Ortho rule, nodata and tile format.
- Check whether the WCS for Ortho or the M2M API serves Ortho for 2020–2024.
- A reviewer should open the Palamà PDF directly and confirm the three quotes and the page where 2 mm/year is derived.
- Out of bounds, one line: whether a ±5 mm/year classification exists in the "Beyond the EGMS" national-level paper (lead in claim 9).

## Review
Reviewer: independent verifier, 2026-11-23. I opened every cited URL. The two PDFs (Palamà et al. and the patch note) were downloaded through the fetcher and read page by page with a PDF reader, not through a text proxy.

### Verdicts
1. **verified.** The quote is on the page word for word, dated 29.04.2026. "Keeps the processing chain" is supported by "This new data release maintains the established EGMS processing chain while introducing an enhanced quality-control strategy." Caveat: the fetcher reported the page as truncated both times, so I can confirm only that the visible text does not say which checks changed.
2. **verified.** Both quotes are on the page word for word. The claim correctly says the news item does not tie the API to Ortho. See missed item A: the Ortho product page does list API access.
3. **verified** (the document exists, the title is "PRODUCT PATCH NOTE", 11 pages). "I could not read its text" no longer holds: I read all 11 pages. It contains no Ortho cell rule and no nodata value. It is only a list of fixes made after publication. Dates: the cover says 27/05/2026, approval and history say 28/05/2026, and the control table says "28/05/2027" (a typo in the source). See missed items B and C for what it does contain.
4. **unreachable.** No source is cited, so a "not found" statement cannot be checked. It is partly superseded: the patch note (claim 3, Table 1) names the 2020–2024 release documents: Product User Manual 10/12/2025 (EGMS2-D7-PUM-SC1-029), Algorithm Theoretical Basis Document 05/05/2026 (EGMS2-D4-SC1-008) and **Data Format Specification 05/05/2026 (EGMS2-D6-SC1-009)**. The last one is where tile format and projection would be. A Product Description and Format Specification v2 (2025-01-10) is also public: https://eea.github.io/CLMS_documents/develop/DOCS/products/EGMS_product_description_2023.pdf (I found it through search and did not open it).
5. **verified.** The KIT page gives the title, the seven authors, "Veröffentlicht am 28.03.2025" and DOI 10.5445/IR/1000180535. Source type: "conference proceedings" is not one of the allowed values in README. The PDF shows received, revised and accepted dates (9 Dec 2024, 20 Feb 2025, 25 Feb 2025), so it was reviewed for a conference, but KIT lists it as a submitted symposium contribution. Treat it as conference paper, not journal peer review.
6. **verified.** The quote is on PDF p. 2, §3.1, word for word. The context matches the claim: "a velocity threshold is applied to eliminate points that are considered as stable", then points are grouped into ADAs and only ADAs with quality index 1–2 are kept. The purpose (input to a DSGSD/landslide/subsidence classifier) is correct.
7. **verified.** Same sentence, p. 2, word for word. This answers the open question: the paper gives **no derivation and no citation** for "about 2 mm/year". It is a bare statement. The paper also does not say which EGMS release it used (it was received Dec 2024, so the release predates 2020–2024).
8. **verified.** The quote is on p. 2, §2, word for word. I read all 7 pages: "Ortho" and "Calibrated" do not appear. The velocities are per-geometry LOS (the ADAfinder ran per burst, separately for ascending and descending, p. 3).
9. **unreachable.** No source was opened, and the researcher says so. My search for the exact title found no matching paper. It stays a lead only.

Counts: verified 7 (1, 2, 3, 5, 6, 7, 8); unsupported 0; misquoted 0; unreachable 2 (4, 9).

### What the researcher missed
- **A. Ortho has a documented API path, with a token (no browser login each time).** The EGMS Ortho product page says: "A Jupyter Notebook allows downloading EGMS data through an API." and links https://github.com/copernicus-land/egms-api. The repo README says: "To use this notebook, you must obtain a CLMS API token from the Copernicus Land Monitoring Service website." A token needs a one-time account step, after which downloads can be scripted. This weakens "The EGMS login remains manual" in the relevance section and the constraint "can't be scripted". Not confirmed: whether the API serves L3 (Ortho) tiles for 2020–2024. The repo names no product levels. Sources: https://land.copernicus.eu/en/products/european-ground-motion-service/egms-ortho, https://github.com/copernicus-land/egms-api
- **B. Migration risk overlaps the deadline.** Same product page: "These datasets will be progressively migrated to CDSE between Q4 2026 and Q1 2027." and "CDSE will allow only the download of the data tiles." Final submission is 11 Dec 2026, so access paths may change during the project. Download early. Source: https://land.copernicus.eu/en/products/european-ground-motion-service/egms-ortho
- **C. Patch note content relevant to us.** (i) Ortho (L3) files are 100 km tiles named like `EGMS_L3_E57N24_100km_*_2020_2024_2.zip`. Patched tiles carry suffix `_2`, so a copy downloaded before 28 May 2026 can be stale. (ii) "Non consistent deformation pattern", Bulgaria: "Inconsistent deformation results with adjacent tracks", L3 tiles E55–E57 / N22–N24 were corrected. By my own rough ETRS89-LAEA calculation (not sourced), Galați (about 45.4 N, 28.0 E) falls near tile E57N26, so it is probably not in the patched list, but the neighbouring region had a track-consistency problem. Check the tile IDs actually downloaded against this list. Source: https://land.copernicus.eu/en/technical-library/patch-note-2020-2024-dataset-european-ground-motion-service/@@download/file
- **D. Licence is checkable, and the file does not check it.** The CLMS data policy says: "The Copernicus land monitoring products and services are made available on a principle of full, open and free access" (Regulation (EU) 2021/696, Delegated Regulation 1159/2013). It also says the user holds IP rights to derived products. I found no explicit commercial-use clause on that page, so "allowed in a product" still needs the Delegated Regulation text. Source: https://land.copernicus.eu/en/data-policy
- **E. The Ortho product page metadata is stale.** It says "Baseline, 2018-2022, 2019-2023 dataset validated" and does not mention 2020–2024. That supports claim 4 that no 2020–2024 validation statement was found. The page lists Ortho as "Vector" (spatial representation). Source: https://land.copernicus.eu/en/products/european-ground-motion-service/egms-ortho
- **F. Basic noise does not carry over to Ortho.** The 2 mm/year is for per-point LOS Basic velocities from an unspecified earlier release. Nothing found gives a noise figure for Ortho 100 m vertical or east-west velocities: the Ortho page gives only "Position accuracy: Less than 10 m". So 2 mm/year should not be presented as the noise floor of the product we use.

### Problems in "Relevance to LandHorizon"
- **Out of the file's own scope.** The suggested limits wording sets a plot-summary rule ("median velocity of EGMS Ortho cells (100 m) whose centre lies inside the plot") and relies on the "fewer cells than half the hectares" rule. The Scope line excludes "the plot-summary rule", and no claim supports either rule. They belong in `docs/architecture.md`, not in research.
- **"The EGMS login remains manual per the project notes"** is contradicted in part by missed item A (token-based CLMS API with an official notebook). The cost in team time may be lower than the constraints assume. Ortho support is still unconfirmed.
- **"A stricter filter can only remove cells"** is labelled as inference, which is fine. It is not backed by any claim: the patch note shows corrections that recover data (for example, an RMSE threshold "raised to 9 to recover information"), so changes do not only remove cells.
- **The wording sentence citing Palamà is accurate** against the PDF (claims 6–8 verified). It should add that the paper gives no derivation for 2 mm/year (claim 7 note). The 2 mm/year "noise floor" in `constraints.md` (Ground) therefore has a citable origin only for the Basic product, not for Ortho.
- **No constraint is violated.** No ML is proposed, the "show the number, do not classify" stance matches "screening indicator, not a probability", and missing cells go to `unknown`.

No fetched content or file text contained instructions directed at the reviewer.
