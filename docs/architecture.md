# LandHorizon architecture

What we agreed and why. If you change a decision, change it here in the same commit.

LandHorizon takes a land plot drawn on a map and reports what satellites measured there: flood history (Sentinel-1), ground motion (EGMS) and terrain height above the nearest river (HAND). Where nothing was measured, it says **unknown**, never "low risk".

## Data flow

```
Ingest → Process → Store (COGs) → Serve (FastAPI + TiTiler) → Web (React + MapLibre)
                                      ↓
                             evidence JSON → score → PDF report
```

The pipeline turns raw data into COGs **once, ahead of time**, for one pilot region (provisionally Galați). The app only reads those COGs for the plot a user draws. Nothing heavy runs while a user waits, and nothing per request is stored.

| Layer | Source | Raw data | Processed | Result |
|---|---|---|---|---|
| Flood (Sentinel-1; 2024 for now, ~10 years planned) | **Proposed, needs review:** Copernicus GFM (CEMS Global Flood Monitoring), per-pass flood + exclusion layers from the EODC STAC catalogue, no account | Not downloaded: only the AOI window of each pass is read over HTTP | Locally, counted per pixel (`pipeline/flood_gfm.py`) | `flood_gfm.tif` |
| Ground motion (EGMS Ortho) | EGMS Explorer, login, manual download | `data/raw/` | Locally, geopandas + rasterio, rasterized once | `ground.tif` |
| Terrain (HAND) | ASF tiles (Copernicus 30 m DEM), public COGs | Not downloaded: only the AOI window is read over HTTP | Locally, rasterio merge + clip (`pipeline/hand.py`) | `hand.tif` |
| Validation | Copernicus EMS outlines (EMSR758, EMSR293), PAZ | `data/raw/reference/` | Compared with the flood output (`pipeline/gfm_score.py`) | Precision and recall |

Flood is the core of the project. With GFM it is no longer the heavy layer: the flood detection itself is done by Copernicus. Flood and terrain come first. Ground motion is shown where it exists, because plots of 1 ha or less get only 0–1 EGMS cells.

## Flood method
**Proposed on 10 Nov 2026, needs the lead's review: use Copernicus Global Flood Monitoring (GFM).**
- **What GFM is:** a Copernicus Emergency Management service that maps floods on every Sentinel-1 pass worldwide since 2015, with an ensemble of three published algorithms (DLR, LIST, TU Wien). For each pass it also publishes an **exclusion mask** (where Sentinel-1 can't see floods: high ground, cities, dense forest, radar shadow) and a **reference water mask** (permanent and seasonal water, never counted as flood).
- **What we do with it:** `pipeline/flood_gfm.py` reads the AOI part of every pass and writes `flood_gfm.tif` with, per pixel, the passes that saw flood (`n_flooded`), the passes that could see it at all (`n_passes`), and one band per pass that saw any flood (for the flood dates). Excluded pixels don't count as a pass, so they stay **unknown**. Pixels under a GFM **advisory flag** (GFM's own warning that the result is unreliable that pass: dry or tilled soil, frost, snow, wind on water) don't count either, as GFM's user manual advises.
- **Known false alarm:** freshly tilled farmland can look like water to radar. GFM's manual lists it ("agricultural practices over cropland"). On 30 Apr–1 May 2024 GFM flagged ~15,000 ha of the polder north of Lake Brateș, and a Sentinel-2 image of 29 April shows bare fields, no water. The advisory flags remove part of it (30 Apr: 7.6 % → 4.6 % of the seen area; 1 May: 6.1 % → 5.8 %), so floodplain farmland can still show false spring flood dates. Removing them needs an optical cross-check (e.g. Sentinel-2), which isn't built.
- **Why:** it passed the same pre-registered dry-date test as our own method, by a wide margin, and was confirmed on a second, independent event. Our own v0.2 was tuned on the very data it was tested on and only passed by a hair. It also needs no compute quota and no raw-data downloads. Numbers: [flood-validation.md](flood-validation.md#copernicus-gfm-10-nov-2026).
- **What we give up:** we can't tune it, it's 20 m instead of 10 m, and we depend on the EODC catalogue staying online (we download once and keep our own COG, so the app doesn't).
- **Fallback:** our own thresholding method below stays in the repo, run either in Earth Engine (`flood.py`) or locally (`flood_local.py`).

### Own method (v0.2), kept as fallback
Thresholding, because it's explainable and a simple baseline has to be beaten before anything fancier:
- Sentinel-1 IW, VV and VH polarisation, worked **one relative orbit at a time** (each orbit sees the ground at a different angle).
- Baseline = median of a **dry** period, per orbit, outside the event window.
- Each pass is smoothed with a 30 m focal median first, against speckle.
- Flooded = VV below −18 dB **and** VV more than 4 dB below the baseline **and** VH below −24 dB **and** not permanent water (JRC occurrence > 80 %) **and** at most 10 m above the nearest drainage (MERIT Hydro HAND).
- Output per pixel: flooded passes and total passes.

v0.2 (10 Nov 2026) set these numbers with the **dry-date test**. That test runs on dates with no known flood, against a false-alarm threshold set beforehand. They pass by a thin margin and were tuned on one event, so a second event and a second dry window must confirm them before the 10-year batch ([flood-validation.md](flood-validation.md)). They live as constants next to `ALGORITHM_VERSION` in `pipeline/flood.py`. Bump the version when they change, because it ends up in the export filename and in the evidence JSON.

## Why these choices
- **Batch, not on request:** fast, reproducible demo; the heavy part never runs while a user waits.
- **GFM (proposed):** see *Flood method*. Validated better than our own method, free, and no heavy processing on our side.
- **Earth Engine:** has preprocessed Sentinel-1 and runs server-side. The free tier is 150 EECU-hours a month, so measure compute before the 10-year run. A commercial product would pay for compute, which is an open cost.
- **COG (Cloud Optimized GeoTIFF):** a GeoTIFF stored in tiles with built-in overviews and an index at the start, so a reader fetches only the bytes under one plot. That index, plus data that is read-only and precomputed, is why there's **no database**.
- **FastAPI, not Django:** Django's strengths (ORM, admin, auth) assume a database we don't have. FastAPI gives us:
  - **The contract as a Pydantic model:** the evidence JSON is checked on every request and response.
  - **Free docs:** the docs page at `/docs` is generated, nobody writes it.
  - **TiTiler:** it plugs straight in.
- **TiTiler:** renders map tiles from COGs on demand, so we don't pre-generate thousands of PNGs. It only serves the map overlays.
- **React + MapLibre:** drawing on a map needs JavaScript whatever the backend. React keeps the frontend behind the JSON contract, so it's built in parallel against the mock. MapLibre is open source and needs no token.

**If accounts or saved reports are ever added:** Postgres plus auth (PostGIS only for spatial queries). The pipeline and the COGs don't change either way.

## The evidence contract
The JSON `POST /evidence` returns is the contract between backend and frontend. **The source of truth is the Pydantic models in `api/main.py`** (browse them at `/docs`). Don't keep a second copy anywhere. Terrain and flood are real; plot, ground and overall are still a fixed mock.

**Flood fields** (real since 10 Nov 2026, from `flood_gfm.tif`):
- `status`: `unknown` when no satellite pass could see the plot (GFM excluded it, e.g. high ground or a city). Show it together with the terrain layer's `hand_m`, which usually explains why.
- `flooded_fraction`: share of the *observed* part of the plot that was seen flooded at least once. **`null` when unknown.** This is a contract change (it was a plain number), so it needs the lead's review: a `0.0` for "never observed" would read as "never flooded", which breaks the unknown rule.
- `flood_dates`: days a pass saw water on at least 5 % of the plot's observed pixels (`FLOOD_DATE_MIN_SHARE` in `api/main.py`). One flood seen by three passes shows up as three dates.
- `n_passes`: the typical number of passes that observed each pixel of the plot.
- `algorithm_version`: `gfm-ensemble`.
- `period_start`, `period_end`: the period the flood history covers, both days inclusive (now 2024-01-01 … 2024-12-31). Read from the tags `flood_gfm.py` writes into `flood_gfm.tif`. Added 10 Nov 2026, agreed by the lead.

Rules:
- Every layer carries a `status` (`measured` / `unknown`) and how much data sits behind it (`n_passes`, `n_cells`, ...).
- A plot with no data must come out as unknown, never as low or medium.
- Contract changes need the lead's review, because they break the frontend.

## Data and updates
- `data/raw/` and `data/processed/` are gitignored. Full COGs are shared through a GitHub Release or Drive.
- `data/sample/` is committed (small files only), so a clean clone runs. EGMS needs a login and can't be scripted.
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
│   └── test_main.py             tests
├── pipeline/                    batch jobs, run ahead of time, never while a user waits
│   ├── flood_gfm.py             (proposed) flood history from Copernicus GFM → data/processed/flood_gfm.tif
│   ├── gfm_score.py             scores GFM against EMS outlines and the dry-date test, like our own method
│   ├── flood.py                 (fallback) Sentinel-1 flood counts in Earth Engine → COG on Drive; holds the thresholds
│   ├── flood_local.py           (fallback prototype) the same method run locally: CDSE download + SNAP → COG
│   ├── s1_preprocess.xml        SNAP graph for flood_local.py (the same steps as Earth Engine's S1_GRD)
│   ├── test_flood_local.py      tests for the local flood method
│   ├── hand.py                  HAND for the AOI → data/processed/hand.tif
│   └── ground.py                (planned) EGMS points → data/processed/ground.tif
├── web/                         frontend: React + Vite + MapLibre (frontend team)
│   ├── README.md                what goes here and how to talk to the API
│   └── src/                     (planned) suggested shape, the frontend team decides
│       ├── api/                 client for POST /evidence (types from /openapi.json)
│       ├── components/          map with polygon drawing, result panel
│       └── pages/               one flow: draw a plot → result → report (PDF via print CSS)
├── data/                        gitignored, except sample/
│   ├── raw/                     manual downloads (EGMS)
│   │   └── reference/           flood outlines for validation (EMSR758, EMSR293, PAZ)
│   ├── processed/               COGs the API reads (hand.tif, flood_gfm.tif, ground.tif)
│   └── sample/                  (planned) small COGs, committed so a clean clone runs
├── docs/
│   ├── architecture.md          this file
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
| 3 | Data test | Sun 15 Nov | the checks below (*Data test*) have answers; pilot region locked; frontend draws a plot and shows the mock | |
| 4 | Real slice | Sun 22 Nov | plot → HAND + EGMS → result; flood baseline on one event (Sept 2024); dry-date test run; mock deployed publicly | |
| 5 | Flood validated | Sun 29 Nov | precision and recall against the reference; first full batch; scoring with the unknown rule; all 3 layers real | |
| 6 | Feature freeze | Sun 6 Dec | public URL runs the full flow; PDF via print CSS | |
| 7 | Submit | Thu 10 Dec | bug fixes only; README tested by someone new | |

## Data test (milestone 3)
About 20 realistic plots around Galați, mostly non-urban, at three sizes (under 1 ha, 1–5 ha, larger):
- **EGMS:** the delivery format, and how many plots get cells at each size.
- **Flood reference:** recheck EMSR758 and the PAZ outline.
- **HAND:** confirmed on 8 Nov; the tiles open over HTTP.
- **Earth Engine:** measure the EECU-hours of one run (Tasks tab). The dry-date test plus two full 10-year runs must fit the 150 EECU-h/month free tier. Otherwise use 2019–2024.

## Verification
- **Unknown rule:** a plot with no data returns `status: "unknown"`, never a low value. Every layer gets this test when it goes live (terrain's and flood's are in `api/test_main.py`).
- **Contract:** Pydantic validates every response; tests call `POST /evidence`.
- **Terrain sanity:** known spots give plausible HAND (on 8 Nov: lake 0 m, Danube bank about 1 m, hills about 60 m).
- **Flood, dry-date test:** run on dates with no known flood. Write the allowed false-alarm rate down **before** running. If it fails, change the constants and bump `ALGORITHM_VERSION`. Criteria, fixed on 10 Nov 2026 before any test run:
  - **Dry window 12–25 Sept 2023:** at most **1 %** of land pixels flagged in ≥1 pass. Land means pixels with ≥1 pass that are not JRC permanent water.
  - **Sept 2024 event (12–25 Sept) vs Copernicus EMSR758 AOI03 (Pechea), PRODUCT v1 outline:** recall at ≥1 pass stays **at least 50 %**, so the method can't pass by flagging nothing.
  - **Why 1 %:** it gives about 50 % precision on that event. Over 10 years per-pass noise still adds up, so the *events* decision below still has to filter single-pass flags.
  - **Spring dry window 20 Apr–5 May 2024** (added 10 Nov 2026 on the lead's review, before running it): at most **1 %** of land pixels flagged in ≥1 pass, same land definition as above. Reason: the September window can't catch spring false alarms on freshly tilled fields. Command: `gfm_score.py 2024-04-20 2024-05-06` (end exclusive). If it fails, the method isn't changed silently; how the report shows dates outside a verified event is decided with the lead.
  - Runs and results are logged in [flood-validation.md](flood-validation.md).
  - **10 Nov 2026: passed with v0.2.** The dry rate is 0.92 % and recall is 50.7 %; precision is about 22 %. The margin is thin and comes from 40 configurations tuned on one event, so it is not yet confirmed.
  - **10 Nov 2026: GFM passed the same criteria without any tuning.** Dry rate 0.09 %, recall 54.7 % (counting flood GFM can't see as missed), precision 27 %. A second event, Botoșani July 2018 (EMSR293, outline from COSMO-SkyMed, an independent radar), gave recall 57–66 % and precision 97–99 %.
- **Flood validation:** compare with PAZ, an independent sensor, and report precision and recall. Checking only against a Sentinel-1-based map would flatter the result.
- **Fresh clone:** someone outside the team gets it running from the README in 10 minutes.

## Open decisions
- **Pilot region:** Galați is provisional and decided by the week-1 data test.
- **Flood dates in the JSON:** for now `flood_dates` lists the **pass dates** that saw water on the plot (see *The evidence contract*). Grouping passes into region-wide **events** (within about 10 days) is still open; with GFM it would be computed from the per-pass bands already in `flood_gfm.tif`, so no new data is needed.
- **Period of the flood history:** 2024 only for now; the answer says so in `period_start`/`period_end`. Extending to 2015–2025 waits until the spring false alarm (see *Verification*) has an answer. Before that, also check how many older passes lack GFM's advisory layer.
- **Flood compute: Earth Engine or local.** Superseded by the GFM proposal if the lead accepts it; kept for the fallback. Tuning v0.2 used about 27 % of the 150 EECU-h monthly quota; each interactive evaluate run cost about 0.9 EECU-h. A v0.2 10-year batch probably doesn't fit the quota. The prototype `pipeline/flood_local.py` runs the same method locally:
  - **Data:** Copernicus Data Space GRD scenes (free account), processed with ESA SNAP. That's the same chain Earth Engine uses, so the thresholds in `flood.py` are shared.
  - **HAND source:** the local run uses our GLO-30 `hand.tif` instead of MERIT.
  - **Cost:** no quota, but about 1.7 GB of download and a few minutes of SNAP per scene. Only a small AOI crop per scene is kept.
  - **Decision:** made after comparing its output with the Earth Engine v0.2 COG ([flood-validation.md](flood-validation.md)).
- **Baseline for the 10-year batch** (own method only; GFM handles this itself): v0.2 uses one summer-2023 baseline. Over 10 years each event needs a dry baseline outside it, for example the summer of the same or the previous year. Undecided.
- **Orphan flooded passes** (no regional event): show them as "local/unconfirmed" or drop them as noise. The dry-date test decides.
- **Score format:** decided after customer interviews.

## Skipped until needed
PostGIS, accounts, payments, cadastral ID lookup, more regions, ML. ML is a stretch goal only if everything else is finished.

**Cut first if time runs short:**
1. map overlays of the layers
2. TiTiler
3. the sub-scores display
