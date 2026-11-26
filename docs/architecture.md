# LandHorizon architecture

What we agreed and why. If you change a decision, change it here in the same commit.

LandHorizon takes a land plot drawn on a map and reports what satellites measured there: flood history (Sentinel-1), ground motion (EGMS) and terrain height above the nearest river (HAND). Where nothing was measured, it says **unknown**, never "low risk".

## Data flow

```
Ingest → Process → Store (COGs) → Serve (FastAPI + TiTiler) → Web (React + MapLibre)
                                      ↓
                             evidence JSON → score → PDF report
```

The pipeline turns raw data into COGs **once, ahead of time**, for one pilot region, Galați (locked on 25 Nov 2026). The app only reads those COGs for the plot a user draws. Nothing heavy runs while a user waits, and nothing per request is stored.

| Layer | Source | Raw data | Processed | Result |
|---|---|---|---|---|
| Flood (Sentinel-1; 2024 for now, ~10 years planned) | Copernicus GFM (CEMS Global Flood Monitoring), per-pass flood + exclusion layers from the EODC STAC catalogue, no account | Not downloaded: only the AOI window of each pass is read over HTTP | Locally, counted per pixel (`pipeline/flood_gfm.py`) | `flood_gfm.tif` |
| Ground motion (EGMS Ortho) | EGMS Explorer, login, manual download | `data/raw/` | Locally, from the CSVs (csv + numpy + rasterio), rasterized once (`pipeline/ground.py`) | `ground.tif` |
| Terrain (HAND) | ASF tiles (Copernicus 30 m DEM), public COGs | Not downloaded: only the AOI window is read over HTTP | Locally, rasterio merge + clip (`pipeline/hand.py`) | `hand.tif` |
| Validation | Copernicus EMS outlines (EMSR758, EMSR293), PAZ | `data/raw/reference/` | Compared with the flood output (`pipeline/gfm_score.py`) | Precision and recall |

Flood is the core of the project. With GFM it is no longer the heavy layer: the flood detection itself is done by Copernicus. Flood and terrain come first. Ground motion is shown where it exists, because plots of 1 ha or less get only 0–1 EGMS cells.

## Flood method
**Copernicus Global Flood Monitoring (GFM): proposed on 10 Nov 2026, accepted by the lead on 11 Nov 2026 as the flood source for now.** It fails the spring false-alarm test (see *Verification*), so how floods are detected and reported is still under review (see *Open decisions*).
- **What GFM is:** a Copernicus Emergency Management service that maps floods on every Sentinel-1 pass worldwide since 2015, with an ensemble of three published algorithms (DLR, LIST, TU Wien). For each pass it also publishes an **exclusion mask** (where Sentinel-1 can't see floods: high ground, cities, dense forest, radar shadow) and a **reference water mask** (permanent and seasonal water, never counted as flood).
- **What we do with it:** `pipeline/flood_gfm.py` reads the AOI part of every pass and writes `flood_gfm.tif` with, per pixel, the passes that saw flood (`n_flooded`), the passes that could see it at all (`n_passes`), and one band per pass that saw any flood (for the flood dates). Excluded pixels don't count as a pass, so they stay **unknown**. Pixels under a GFM **advisory flag** (GFM's own warning that the result is unreliable that pass: dry or tilled soil, frost, snow, wind on water) don't count either, as GFM's user manual advises. A scene with **no advisory layer at all** isn't seen either (decision 1a, below).
- **Known false alarm:** freshly tilled farmland can look like water to radar. GFM's manual lists it ("agricultural practices over cropland"). On 30 Apr–1 May 2024 GFM flagged ~15,000 ha of the polder north of Lake Brateș, and a Sentinel-2 image of 29 April shows bare fields, no water. The advisory flags remove part of it (30 Apr: 7.6 % → 4.6 % of the seen area; 1 May: 6.1 % → 5.8 %), so floodplain farmland can still show false spring flood dates. Removing them needs an optical cross-check (e.g. Sentinel-2), which isn't built.
- **Why:** it passed the same pre-registered September dry-date test as our own method, by a wide margin, and was confirmed on a second, independent event. It fails the spring window that was added later. Our own v0.2 was tuned on the very data it was tested on and only passed by a hair. It also needs no compute quota and no raw-data downloads. Numbers: [flood-validation.md](flood-validation.md#copernicus-gfm-10-nov-2026).
- **What we give up:** we can't tune it, it's 20 m instead of 10 m, and we depend on the EODC catalogue staying online (we download once and keep our own COG, so the app doesn't).
- **Fallback:** our own thresholding method below stays in the repo, run either in Earth Engine (`flood_earthengine.py`) or locally (`flood_local.py`).

### Own method (v0.2), kept as fallback
Thresholding, because it's explainable and a simple baseline has to be beaten before anything fancier:
- Sentinel-1 IW, VV and VH polarisation, worked **one relative orbit at a time** (each orbit sees the ground at a different angle).
- Baseline = median of a **dry** period, per orbit, outside the event window.
- Each pass is smoothed with a 30 m focal median first, against speckle.
- Flooded = VV below −18 dB **and** VV more than 4 dB below the baseline **and** VH below −24 dB **and** not permanent water (JRC occurrence > 80 %) **and** at most 10 m above the nearest drainage (MERIT Hydro HAND).
- Output per pixel: flooded passes and total passes.

v0.2 (10 Nov 2026) set these numbers with the **dry-date test**. That test runs on dates with no known flood, against a false-alarm threshold set beforehand. They pass by a thin margin and were tuned on one event, so a second event and a second dry window must confirm them before the 10-year batch ([flood-validation.md](flood-validation.md)). They live as constants next to `ALGORITHM_VERSION` in `pipeline/flood_earthengine.py`. Bump the version when they change, because it ends up in the export filename and in the evidence JSON.

## Why these choices
- **Batch, not on request:** fast, reproducible demo; the heavy part never runs while a user waits.
- **GFM:** see *Flood method*. Validated better than our own method on the September tests, free, and no heavy processing on our side.
- **Earth Engine:** has preprocessed Sentinel-1 and runs server-side. The free tier is 150 EECU-hours a month, so measure compute before the 10-year run. A commercial product would pay for compute, which is an open cost.
- **COG (Cloud Optimized GeoTIFF):** a GeoTIFF stored in tiles with built-in overviews and an index at the start, so a reader fetches only the bytes under one plot. That index, plus data that is read-only and precomputed, is why there's **no database**.
  - **`flood_gfm.tif` has no overviews** (26 Nov 2026, F3; approved by Sover, to be reviewed by the lead in the F3+F6 PR). It's still a COG, tiled with the index first, and the values don't change.
    - **Why:** at the 10-year size (~1,200 bands, synthetic test), GDAL's overview step at the end of `flood_gfm.py` ran over 49 min on one core without finishing; without overviews the COG copy took 5.7 min ([flood-validation.md](flood-validation.md#flood-history-2015--13-apr-2025-f3-26-nov-2026)).
    - **Nothing needs them today:** `api/main.py` reads full-resolution windows only. The old overviews were cubic-resampled, which means nothing on 0/1 flood bands and pass counts.
    - **When to revert:** if TiTiler or any map view of the flood layer is added (it would read overviews when zoomed out).
    - **How to revert:** delete `OVERVIEWS="NONE"` from the `rio_copy` call at the end of `pipeline/flood_gfm.py` (or `git revert` the commit "flood_gfm: write flood_gfm.tif without COG overviews"), then rebuild. Use nearest resampling (`OVERVIEW_RESAMPLING="NEAREST"`), not GDAL's cubic default, and expect the final write to take an hour or more at ~1,200 bands. Faster option: add the overviews afterwards, to a copy of the file, only for the bands the map shows.
  - `hand.tif` and `ground.tif` keep their overviews.
- **FastAPI, not Django:** Django's strengths (ORM, admin, auth) assume a database we don't have. FastAPI gives us:
  - **The contract as a Pydantic model:** the evidence JSON is checked on every request and response.
  - **Free docs:** the docs page at `/docs` is generated, nobody writes it.
  - **TiTiler:** it plugs straight in.
- **TiTiler:** renders map tiles from COGs on demand, so we don't pre-generate thousands of PNGs. It only serves the map overlays.
- **React + MapLibre:** drawing on a map needs JavaScript whatever the backend. React keeps the frontend behind the JSON contract, so it's built in parallel against the mock. MapLibre is open source and needs no token.
- **Frontend details (PR #5, merged 19 Nov 2026; the frontend team decides, [web/README.md](../web/README.md)):** TypeScript on Vite, with the client types generated from `/openapi.json` (`openapi-typescript`) so the contract isn't copied by hand; Tailwind for the layout and the `@media print` styles behind the PDF; a picker for the 20 test plots in `data/sample/plots.geojson`; a mock mode for working without the COGs. The website code lives in its own repo, `EchipaTeams/demo-repository`.
- **Mock mode (agreed on the lead's review of PR #5, 19 Nov 2026):**
  - **A manual toggle only, never an automatic fallback.** `MOCK` looks measured (flood `measured`, 42 % flooded, HAND 1.7 m). A UI that fell back to it whenever the API failed would show fake data as real, which breaks the unknown rule. It would happen often, because the API answers 503 while a COG is missing.
  - **While it is on**, every view and the printed PDF show a visible **MOCK** label.
  - **With it off**, a 503 is shown as a server error, never as mock data and never as `unknown` (unknown means the satellites didn't see the plot).
  - **No second copy:** the website's mock JSON is exported from `MOCK` in `api/main.py`, not hand-written (command in [web/README.md](../web/README.md#generated-files)).

**If accounts or saved reports are ever added:** Postgres plus auth (PostGIS only for spatial queries). The pipeline and the COGs don't change either way.

## The evidence contract
The JSON `POST /evidence` returns is the contract between backend and frontend. **The source of truth is the Pydantic models in `api/main.py`** (browse them at `/docs`). Don't keep a second copy anywhere. Terrain, flood, ground and plot are real; overall is still a fixed mock, because its format waits for the customer interviews. Its one reason says exactly that, because a fixed reason about the layers (it used to say "no ground-motion cells under plot") contradicts plots where ground is measured.

**Flood fields** (real since 10 Nov 2026, from `flood_gfm.tif`):
- `status`: `unknown` when satellite passes could see less than half of the plot (GFM excluded the rest, e.g. high ground or a city). Show it together with `observed_fraction` and the terrain layer's `hand_m`, which usually explains why.
- `observed_fraction`: share of the plot's pixels that at least one pass could see, 0 to 1. Filled for unknown plots too. Below `MIN_OBSERVED_FRACTION` (0.5, in `api/main.py`) the plot is `unknown`, because what was seen on one corner doesn't describe the plot. The cost: a plot that was flooded in its small visible part reports unknown, not flooded. The 0.5 is a judgment call, to be checked on the 20 test plots. Added 11 Nov 2026 by the lead (a contract change).
- `flooded_fraction`: share of the *observed* part of the plot that was seen flooded at least once. **`null` when unknown** (a contract change of 10 Nov 2026; it was a plain number): a `0.0` for "never observed" would read as "never flooded", which breaks the unknown rule.
- `flood_dates`: days a pass saw water on at least 5 % of the plot's observed pixels (`FLOOD_DATE_MIN_SHARE` in `api/main.py`). One flood seen by three passes shows up as three dates.
- `n_passes`: the typical number of passes that observed each observed pixel of the plot. Filled for a barely observed plot too; 0 only when nothing was seen.
- `algorithm_version`: `gfm-ensemble`.
- `period_start`, `period_end`: the period the flood history covers, both days inclusive (now 2024-01-01 … 2024-12-31). Read from the tags `flood_gfm.py` writes into `flood_gfm.tif`. Added 10 Nov 2026, agreed by the lead.

**Ground fields** (real since 16 Nov 2026, from `ground.tif`; the shape of the model didn't change):
- `n_cells`: EGMS cells (100 m) **with data** whose **centre is inside the plot**, the same rule as `pipeline/ground.py --plots`. Flood and terrain take every pixel a plot touches; for 100 m cells that would give a 0.5 ha plot the motion of a building next to it. It is filled when the status is `unknown` for lack of cells too, as flood keeps `n_passes`, so the answer says how much data sits behind it. Since 23 Nov 2026 `unknown` no longer means 0 cells: a plot can be `unknown` with `n_cells` 1.
- `velocity_mm_yr`: median vertical velocity of those cells, in mm/yr (negative = sinking), to 0.1 as EGMS delivers it.
- `status`: `unknown`, with `velocity_mm_yr` `null`, when less than half of the cells whose centre is inside the plot have data (`GROUND_MIN_SHARE`, 0.5, in `api/main.py`), and when no cell has its centre inside (`n_cells` 0). Never 0 mm/yr. Exactly half counts as `measured`. Until 23 Nov 2026 one cell was enough, so a plot holding several cells got the motion of the one that had data. The 0.5 mirrors `MIN_OBSERVED_FRACTION` and `TERRAIN_MIN_SHARE`. Proposed 23 Nov 2026, accepted by the lead on 25 Nov 2026 (L3) with this denominator. The alternative, max(1, round(`area_ha`)), was compared on the real `ground.tif` (`checks/ground_share/compare.py`): the two agree on all 20 test plots and on 97 % of 9,600 rectangles placed on cells with data. Where they differ, the area denominator is looser on plots of 2 ha or less (1 cell with data out of 3 or 4 that fit counts as `measured`) and depends on where the plot sits on the 100 m grid. On farmland `unknown` is the usual answer: 18 of the 20 test plots, none of them changed by the share (`edge-50`, 1 of 2 cells, and `edge-65`, 4 of 8, stay `measured`).
- `release`: the EGMS release behind the answer (now `2020-2025`), read from the tag `ground.py` writes into `ground.tif`. Filled for unknown plots too.

**Plot fields** (real since 16 Nov 2026):
- `area_ha`: the polygon's area in hectares, to 0.01, computed in EPSG:3035 (equal-area), holes subtracted.
- `n_pixels` (reading accepted by the lead on 19 Nov 2026): the pixels of the flood grid (10 m) the plot touches, the ones `flood.observed_fraction` is a share of. It tells how many flood measurements fit on the plot. Because a touched pixel counts whole, it is more than `area_ha` × 100: 89 for the 0.60 ha test plot `flood-pechea-1`. The docs didn't define it before; the mock (0.8 ha, 80 px) fits a 10 m grid.

**Terrain fields** (from `hand.tif`; the shape of the model didn't change):
- `hand_m`: median HAND (height above the nearest drainage) of the plot's pixels with data, in m, to 0.1. Every pixel the plot touches counts, as for flood.
- `status`: `unknown`, with `hand_m` `null`, when less than half of the plot's pixels have HAND data (`TERRAIN_MIN_SHARE`, 0.5, in `api/main.py`). Until 20 Nov 2026 one pixel with data was enough, so a plot with data on one corner got that corner's height. The 0.5 mirrors flood's `MIN_OBSERVED_FRACTION`. `hand.tif` has data on the whole AOI today, so none of the 20 test plots changes. Proposed 20 Nov 2026, accepted by the lead on 21 Nov 2026 (PR #9).

**A plot not wholly inside every layer is refused** (proposed 20 Nov 2026, accepted by the lead on 21 Nov 2026, PR #9): `POST /evidence` answers 422 when any part of the plot is outside a layer's raster, with a message naming the layer. Before, only a plot wholly outside was refused. A plot across the edge was answered from the part inside, and nothing said so: its `flood.observed_fraction` and `plot.n_pixels` counted only that part. The check compares the plot's bounds with each raster's bounds in the raster's own CRS, before any pixel is read. `hand.tif` covers exactly the AOI and the other layers reach a little beyond it, so in practice the AOI's edge decides. The closest of the 20 test plots is about 1.2 km inside it.

Rules:
- Every layer carries a `status` (`measured` / `unknown`) and how much data sits behind it (`n_passes`, `n_cells`, ...).
- A plot with no data must come out as unknown, never as low or medium.
- Contract changes need the lead's review, because they break the frontend.

## Data and updates
- `data/raw/` and `data/processed/` are gitignored. The COGs the API reads (`hand.tif`, `flood_gfm.tif`, `ground.tif`) are shared on the **team Drive**: copy them into `data/processed/`. The API answers 503 while one is missing, so this is the first step after cloning (README, *Run it*). It matters most for `ground.tif`: EGMS needs a login and can't be scripted.
- `data/sample/` is committed (small files only): the 20 test plots. `api/test_main.py` builds its own tiny rasters, so `uv run pytest` passes on a clean clone; `api/test_plots.py` is skipped until the three COGs are in place.
- The deployed server reads COGs from a Docker volume or bucket URL.
- **For the demo the data is frozen**, so validation and pitch numbers stay fixed. The pipeline stays one re-runnable command with a date range.
- **In a real product:** a separate scheduled job, not the web app, processes new passes into a new versioned COG.

## Working agreements
- **Python 3.14, dependencies with uv:**
  - Run `uv sync` after pulling, and `uv add <pkg>` to add a package.
  - Commit `uv.lock`.
  - Don't use pip.
- **Never commit:**
  - secrets (`gee-key.json`, `*-key.json`, `.env`)
  - large data
  - **any AIM-Space data** (course rule, `aim-space/` is gitignored)
- **Push to `main` while it's one person.** Once teammates push, use short branches and squash-merged PRs, with pairs reviewing each other.
- **Build the minimum:**
  - no scaffolding for later
  - a folder appears when its first real file does
  - tests on core logic only
- **Bus factor:** everyone should be able to explain the data, method, code and results.

## Repository layout
`(planned)` = agreed, but the file or folder doesn't exist yet. It appears with its first real file.

```
LandHorizon/
├── api/                         backend: FastAPI
│   ├── main.py                  evidence contract (Pydantic) + POST /evidence; TiTiler mounts here later
│   ├── test_main.py             tests
│   └── test_plots.py            the 20 test plots against the real layers (skipped without all three); prints the data-test table
├── pipeline/                    batch jobs, run ahead of time, never while a user waits
│   ├── flood_gfm.py             flood history from Copernicus GFM → data/processed/flood_gfm.tif
│   ├── flood_common.py          shared by the flood scripts: AOI and grid, water masks, EMS references, scoring
│   ├── test_flood_common.py     tests for the shared helpers
│   ├── gfm_score.py             scores GFM against EMS outlines and the dry-date test, like our own method
│   ├── flood_earthengine.py     (fallback) Sentinel-1 flood counts in Earth Engine → COG on Drive; holds the thresholds
│   ├── flood_local.py           (fallback prototype) the same method run locally: CDSE download + SNAP → COG
│   ├── s1_preprocess.xml        SNAP graph for flood_local.py (the same steps as Earth Engine's S1_GRD)
│   ├── test_flood_local.py      tests for the local flood method
│   ├── hand.py                  HAND for the AOI → data/processed/hand.tif
│   └── ground.py                EGMS Ortho U CSVs → data/processed/ground.tif
├── web/                         frontend decisions; the code is in EchipaTeams/demo-repository (React + TypeScript + Vite + Tailwind + MapLibre)
│   └── README.md                frontend decisions, generated types and mock, how the website talks to the API
├── data/                        gitignored, except sample/
│   ├── raw/                     manual downloads (EGMS)
│   │   └── reference/           flood outlines for validation (EMSR758, EMSR293, PAZ)
│   ├── processed/               COGs the API reads (hand.tif, flood_gfm.tif, ground.tif), copied from the team Drive
│   └── sample/                  small files, committed: plots.geojson (the 20 test plots); small COGs (planned)
├── docs/
│   ├── architecture.md          this file
│   ├── evidence-request.md      how the website sends a plot to POST /evidence and handles the answers
│   └── flood-validation.md      flood test runs and their results
├── docker-compose.yml           (planned, W4) API + web for the deployment
├── pyproject.toml               Python dependencies (uv)
├── uv.lock                      exact pinned versions, committed
├── AGENTS.md                    rules for AI assistants and new teammates
├── CLAUDE.md                    points Claude to AGENTS.md
└── README.md                    what it is + how to run it
```

## Milestones
Engineering only. Dates come from the team plan.

| # | Milestone | By | Done when | Status |
|---|---|---|---|---|
| 1 | Skeleton | 8 Nov | repo, uv, contract + mock endpoint, these docs | done |
| 2 | Terrain | 8 Nov | `POST /evidence` returns real HAND under the polygon | done |
| 3 | Data test | Sun 15 Nov | the checks below (*Data test*) have answers; pilot region locked; frontend draws a plot and shows the mock | Done, except the frontend check: data-test answers 13 Nov, Galați locked 25 Nov; the website's mock flow is checked in L8 |
| 4 | Real slice | Sun 22 Nov | plot → HAND + EGMS → result; flood baseline on one event (Sept 2024); dry-date test run; mock deployed publicly | Done, except the public deploy: plot → HAND + EGMS 16 Nov (#6), Sept 2024 flood and dry-date test 10 Nov; the deploy is due 27 Nov (G4) |
| 5 | Flood validated | Sun 29 Nov | precision and recall against the reference; first full batch; scoring with the unknown rule; all 3 layers real | |
| 6 | Feature freeze | Sun 6 Dec | public URL runs the full flow; PDF via print CSS | |
| 7 | Submit | Thu 10 Dec | bug fixes only; README tested by someone new | |

## Data test (milestone 3)
About 20 realistic plots around Galați, mostly non-urban, at three sizes (under 1 ha, 1–5 ha, larger):
- **EGMS:** the delivery format, and how many plots get cells at each size. Answered on 13 Nov 2026:
  - **Format:** EGMS Explorer → Product Archive (login), Ortho (Level 3), Vertical (U), release 2020–2025. One zip per 100 km tile, holding a CSV, a TIFF and a small XML (metadata only). The AOI needs two tiles, E56N26 and E57N26: about 58 MB zipped, 240 MB unzipped. The CSV has `easting`, `northing`, `mean_velocity` (mm/yr, rounded to 0.1), `mean_velocity_std` and more, then one column per date; EPSG:3035, 100 m grid, cell centres end in 50 m.
  - **The E57N26 TIFF is one cell off:** EGMS georeferenced it 100 m east and 100 m south of its tile name, so its values land on the neighbouring cell. The E56N26 TIFF is correct. That's why `pipeline/ground.py` reads the CSVs. E57N26 was produced later (16 Oct 2026, E56N26 on 28 Jul 2026, per the XML), so recheck it if the tiles are downloaded again.
  - **Coverage:** `ground.tif` has 41,181 cells with data, about 9 % of the AOI grid; velocity −17.8 to +16.4 mm/yr, median −0.6. Cells sit on buildings, roads and villages; fields, water and wetland are mostly empty.
  - **Cells per plot** (`uv run python pipeline/ground.py --plots data/sample/plots.geojson`; a cell counts when its centre is inside the plot): under 1 ha, 0 of 7 plots get a cell with data; 1–5 ha, 1 of 8; over 5 ha, 1 of 5 (0.0 / 0.1 / 0.8 cells with data per plot). The two are `edge-50` (1.9 ha, 1 cell) and `edge-65` (7.5 ha, 4 cells). All 20 plots are farmland, grass or wetland, so for non-urban plots ground motion is usually **unknown**, as expected for a layer shown "where it exists".
  - **Cells that fit, and the share with data** (25 Nov 2026; the API decides a plot's status from this share, so `--plots` now prints it, but only reports it: the threshold lives in `api/main.py`). Same command. The cells whose centre is inside a plot, empty ones included, are 0.7 / 2.2 / 15.6 per plot (under 1 ha / 1–5 ha / over 5 ha); the ones with data are 0.0 / 0.1 / 0.8, so the share with data is 0 % / 6 % / 5 % of the cells that fit. Two plots, `plateau-1` and `water-edge-1`, are smaller than a cell: no cell has its centre inside (0 of 0, share not defined, unknown). `edge-50` is 1 of 2 cells (50 %) and `edge-65` is 4 of 8 (50 %); the other 16 plots with a cell inside have 0 with data.
  - **In the API (16 Nov 2026):** `POST /evidence` uses the same rule, a cell's centre inside the plot (`read_plot(..., all_touched=False)` in `api/main.py`), and gives the same cells and medians for all 20 plots: `edge-50` 1 cell, −4.6 mm/yr; `edge-65` 4 cells, 0.4 mm/yr; the other 18 unknown.
  - **With the share rule** (`GROUND_MIN_SHARE` 0.5 in `api/main.py`, merged in #11; checked on 25 Nov 2026 by calling `ground()` on the 20 plots with that `api/main.py` and the real `ground.tif`): `edge-50` and `edge-65` stay `measured` (`n_cells` 1 and 4, −4.6 and 0.4 mm/yr), the other 18 stay `unknown`. Both sit **exactly at** the 0.5 threshold, 50 % each, and exactly at it counts as measured: a threshold above 0.5 would turn both `unknown`, and no test plot would be `measured`.
- **Flood reference:** recheck EMSR758 and the PAZ outline.
- **HAND:** confirmed on 8 Nov; the tiles open over HTTP.
- **Earth Engine:** measure the EECU-hours of one run (Tasks tab). The dry-date test plus two full 10-year runs must fit the 150 EECU-h/month free tier. Otherwise use 2019–2024.

## Verification
- **Unknown rule:** a plot with no data returns `status: "unknown"`, never a low value. Every layer gets this test when it goes live (terrain's, flood's and ground's are in `api/test_main.py`).
- **Contract:** Pydantic validates every response; tests call `POST /evidence`.
- **Terrain sanity:** known spots give plausible HAND (on 8 Nov: lake 0 m, Danube bank about 1 m, hills about 60 m).
- **Flood, dry-date test:** run on dates with no known flood. Write the allowed false-alarm rate down **before** running. If it fails, change the constants and bump `ALGORITHM_VERSION`. Criteria, fixed on 10 Nov 2026 before any test run:
  - **Dry window 12–25 Sept 2023:** at most **1 %** of land pixels flagged in ≥1 pass. Land means pixels with ≥1 pass that are not JRC permanent water.
  - **Sept 2024 event (12–25 Sept) vs Copernicus EMSR758 AOI03 (Pechea), PRODUCT v1 outline:** recall at ≥1 pass stays **at least 50 %**, so the method can't pass by flagging nothing.
  - **Why 1 %:** it was expected to give about 50 % precision on that event; the measured precision is 22–27 %. Over 10 years per-pass noise still adds up, so the *events* decision below still has to filter single-pass flags.
  - **Spring dry window 20 Apr–5 May 2024** (added 10 Nov 2026 on the lead's review, before running it): at most **1 %** of land pixels flagged in ≥1 pass, same land definition as above. Reason: the September window can't catch spring false alarms on freshly tilled fields. Command: `gfm_score.py 2024-04-20 2024-05-06` (end exclusive). If it fails, the method isn't changed silently; how the report shows dates outside a verified event is decided with the lead.
  - **Spring window on GFM v4, 20 Apr–5 May 2025** (added 24 Nov 2026, before running it): same false-alarm limit and land definition, at most **1 %** of land pixels flagged in ≥1 pass. It asks whether the spring 2024 false alarm repeats in v4; it can't validate v4 (no v4 flood with a reference outline is known), and the history stops before v4, so nothing in it depends on the result. Command: `gfm_score.py 2025-04-20 2025-05-06` (end exclusive).
    - **Dryness check, before the run:** no flood on record in Galați County, and a clear Sentinel-2 image checked by eye.
    - **Dry, above 1 %:** v4 fails the spring test too. It's put down to tilled fields only if the Sentinel-2 images show bare fields where the flags are; otherwise the cause is unknown (v4 also keeps small patches that v3 removed).
    - **Dry, 1 % or less:** it didn't repeat in this window. That doesn't show v4 fixed it: the year, the fields and the soil moisture differ, and there is no v3 run of 2025 to compare with.
    - **Not dry, or the check can't be done:** inconclusive, whatever the percentage.
    - The method isn't changed on this result.
  - Runs and results are logged in [flood-validation.md](flood-validation.md).
  - **10 Nov 2026: passed with v0.2.** The dry rate is 0.92 % and recall is 50.7 %; precision is about 22 %. The margin is thin and comes from 40 configurations tuned on one event, so it is not yet confirmed.
  - **10 Nov 2026: GFM passed the two September criteria without any tuning.** Dry rate 0.09 %, recall 54.7 % (counting flood GFM can't see as missed), precision 27 %. A second event, Botoșani July 2018 (EMSR293, outline from COSMO-SkyMed, an independent radar), gave recall 57–66 % and precision 97–99 %.
  - **11 Nov 2026: GFM fails the spring window.** 9.06 % of land flagged in ≥1 pass against the 1 % limit, almost all of it on 30 Apr and 1 May 2024. The method was not changed to make it pass. What to do about it is in *Open decisions*.
  - **26 Nov 2026: every test re-scored under decision 1a** (no advisory layer = not seen). Galați, the September dry window and the spring window are unchanged, because no 2023 or 2024 scene lacks the layer. Botoșani loses the 2 July 16:00 pass: recall 55–64 % counting flood GFM can't see as missed (was 57–66 %), precision still 97–99 %.
  - **25 Nov 2026: GFM v4 fails the spring 2025 window.** 15.81 % of land flagged in ≥1 pass against the 1 % limit. The cause is unknown: 98 % of the flags lie outside the polder, mostly on green land, so tilled fields don't explain them. The window was checked dry on the polder before the run; the land under the other 98 % was looked at only after it, and water under dense crops wouldn't show. The method was not changed; the history stops before v4 (decision 1b, *Period of the flood history*).
- **Flood validation:** compare with outlines from independent sensors and report precision and recall. Checking only against a Sentinel-1-based map would flatter the result. Done for EMSR758 (Galați: PAZ and COSMO-SkyMed SG) and EMSR293 (Botoșani: COSMO-SkyMed); none of them is Sentinel-1.
- **Fresh clone:** someone outside the team gets it running from the README in 10 minutes.

## Open decisions
- **Segment (gate, 22 Nov):** not decided. It waits for the interview summary; until then the product stays aimed at land buyers.
- **Law option (gate, 22 Nov):** provisional, until the law wording is checked with Simonel at the SAR workshop (26 Nov).
- **Flood dates in the JSON:** for now `flood_dates` lists the **pass dates** that saw water on the plot (see *The evidence contract*). Grouping passes into region-wide **events** (within about 10 days) is still open; with GFM it would be computed from the per-pass bands already in `flood_gfm.tif`, so no new data is needed.
- **False flood dates outside real floods** (under review; the lead researches detection methods on 11 Nov 2026). GFM fails the spring test, so on floodplain farmland `flood_dates` and `flooded_fraction` can include tilled-soil false alarms, and the report can't present every date as a confirmed flood. To check:
  - **A verified-event list.** Only pass dates inside a list of confirmed floods (for 2024: 12–25 Sept, EMSR758) count as flood. Other dates are reported separately as unverified, and `flooded_fraction` counts the verified passes only. It needs no new data: the per-pass bands are already in `flood_gfm.tif`. **Not adopted:**
    - The list is kept by hand, which defeats the purpose of an automatic product.
    - It is region-wide, not per plot: inside that window Galați precision was 27 %.
    - A real flood without an EMS activation would land in unverified.
  - **What doesn't remove it:** grouping passes into events (two orbits saw the false alarm on consecutive days) and requiring ≥2 passes (still 2.17 %, and it costs flash-flood recall).
  - **An optical cross-check** (e.g. Sentinel-2 NDWI): not built.
- **Period of the flood history:** 2024 only until the 2015 – 13 Apr 2025 build is on the Drive (week 3); the answer says so in `period_start`/`period_end`. The spring false alarm (above) isn't solved: the lead scheduled the build with a farmland caveat shown next to flood dates. Two rules decided by the lead apply to it:
  - **1a, no advisory layer = not seen** (17 Nov 2026). A missing layer isn't "no warnings": 224 of 9,102 scenes over 2015–2025 have none, none of them in 2022–2024 ([flood-validation.md](flood-validation.md)). `gfm_score.passes()` drops that scene only; its neighbours in the same pass still count. If GFM publishes a missing layer, the next build picks the scene up. Roadmap: a weather-based stand-in for the missing warnings.
  - **1b, one major GFM version** (13 Nov 2026). Layers from different major versions can't be used together, so `flood_gfm.py` stops the history on the day the major version in the catalogue's `processing:version` changes: over this AOI v3.1.0 ends on 13 Apr 2025 and v4.0.0 starts on 14 Apr. `period_end` follows from that, not from a fixed date. Each pass's version, and the algorithms that contributed to all its scenes that counted (`flood_members`; a pass where none counted isn't listed), are in the `gfm_versions` tag of `flood_gfm.tif`; the API contract doesn't change.
- **Flood compute: Earth Engine or local.** Superseded by GFM for now; kept for the fallback. Tuning v0.2 used about 27 % of the 150 EECU-h monthly quota; each interactive evaluate run cost about 0.9 EECU-h. A v0.2 10-year batch probably doesn't fit the quota. The prototype `pipeline/flood_local.py` runs the same method locally:
  - **Data:** Copernicus Data Space GRD scenes (free account), processed with ESA SNAP. That's the same chain Earth Engine uses, so the thresholds in `flood_earthengine.py` are shared.
  - **HAND source:** the local run uses our GLO-30 `hand.tif` instead of MERIT.
  - **Cost:** no quota, but about 1.7 GB of download and a few minutes of SNAP per scene. Only a small AOI crop per scene is kept.
  - **Decision:** made after comparing its output with the Earth Engine v0.2 COG ([flood-validation.md](flood-validation.md)).
- **Baseline for the 10-year batch** (own method only; GFM handles this itself): v0.2 uses one summer-2023 baseline. Over 10 years each event needs a dry baseline outside it, for example the summer of the same or the previous year. Undecided.
- **Orphan flooded passes** (no regional event): show them as "local/unconfirmed" or drop them as noise. The dry-date test decides.
- **Score format (decided 25 Nov 2026 by the lead):** no number. `overall` gives a status for flood, a status for terrain and one status for both, each with its reasons. Ground stays out of it, because it is shown only where it exists. A core layer that is `unknown` gives `incomplete`, never a low value. The status values and the model's new shape come with the change to `overall` (L7), which changes the contract.

## Skipped until needed
PostGIS, accounts, payments, cadastral ID lookup, more regions, ML. ML is a stretch goal only if everything else is finished.

**Cut first if time runs short:**
1. map overlays of the layers
2. TiTiler
3. the sub-scores display
