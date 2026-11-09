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
| Flood (Sentinel-1, ~10 years) | Earth Engine `COPERNICUS/S1_GRD` | Stays on Google's servers | Inside Earth Engine (`pipeline/flood.py`) | Flood COG(s), exported to Drive |
| Ground motion (EGMS Ortho) | EGMS Explorer, login, manual download | `data/raw/` | Locally, geopandas + rasterio, rasterized once | `ground.tif` |
| Terrain (HAND) | ASF tiles (Copernicus 30 m DEM), public COGs | Not downloaded: only the AOI window is read over HTTP | Locally, rasterio merge + clip (`pipeline/hand.py`) | `hand.tif` |
| Validation | Copernicus EMS outlines, PAZ | `data/raw/reference/` | Compared with the flood output | Precision and recall |

Flood is the only heavy layer and the core of the project. Flood and terrain come first. Ground motion is shown where it exists, because plots of 1 ha or less get only 0–1 EGMS cells.

## Flood method
Thresholding, because it's explainable and a simple baseline has to be beaten before anything fancier:
- Sentinel-1 IW, VV polarisation, worked **one relative orbit at a time** (each orbit sees the ground at a different angle).
- Baseline = median of a **dry** period, per orbit, outside the event window.
- Flooded = darker than about −18 dB **and** more than about 3 dB darker than the baseline **and** not permanent water (JRC occurrence > 80 %).
- Output per pixel: flooded passes and total passes.

The numbers are placeholders. The **dry-date test** (run on dates with no known flood, with a false-alarm threshold set beforehand) and validation fix them before the full batch. They live as constants next to `ALGORITHM_VERSION` in `pipeline/flood.py`. Bump the version when they change, because it ends up in the export filename and in the evidence JSON.

## Why these choices
- **Batch, not on request:** fast, reproducible demo; the heavy part never runs while a user waits.
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
The JSON `POST /evidence` returns is the contract between backend and frontend. **The source of truth is the Pydantic models in `api/main.py`** (browse them at `/docs`). Don't keep a second copy anywhere. Until the real data is wired in, the endpoint returns a fixed mock.

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
│   ├── flood.py                 Sentinel-1 flood counts in Earth Engine → COG on Drive
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
│   │   └── reference/           flood outlines for validation (EMSR758, PAZ)
│   ├── processed/               COGs the API reads (hand.tif, flood, ground.tif)
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
- **Unknown rule:** a plot with no data returns `status: "unknown"`, never a low value. Every layer gets this test when it goes live (terrain's is in `api/test_main.py`).
- **Contract:** Pydantic validates every response; tests call `POST /evidence`.
- **Terrain sanity:** known spots give plausible HAND (on 8 Nov: lake 0 m, Danube bank about 1 m, hills about 60 m).
- **Flood, dry-date test:** run on dates with no known flood. Write the allowed false-alarm rate down **before** running. If it fails, change the constants and bump `ALGORITHM_VERSION`. Criteria, fixed on 10 Nov 2026 before any test run:
  - **Dry window 12–25 Sept 2023:** at most **1 %** of land pixels flagged in ≥1 pass. Land means pixels with ≥1 pass that are not JRC permanent water.
  - **Sept 2024 event (12–25 Sept) vs Copernicus EMSR758 AOI03 (Pechea), PRODUCT v1 outline:** recall at ≥1 pass stays **at least 50 %**, so the method can't pass by flagging nothing.
  - **Why 1 %:** it gives about 50 % precision on that event. Over 10 years per-pass noise still adds up, so the *events* decision below still has to filter single-pass flags.
  - Runs and results are logged in [flood-validation.md](flood-validation.md).
  - **10 Nov 2026:** not passed yet. With a speckle filter, a HAND mask and a stricter drop, the best result is a 1.11 % dry rate at 51 % recall, or 0.80 % at 49 %. The constants stay at v0.1 until a setting passes.
- **Flood validation:** compare with PAZ, an independent sensor, and report precision and recall. Checking only against a Sentinel-1-based map would flatter the result.
- **Fresh clone:** someone outside the team gets it running from the README in 10 minutes.

## Open decisions
- **Pilot region:** Galați is provisional and decided by the week-1 data test.
- **Flood dates in the JSON:** one flood is seen by several passes over several days, so the proposal is to group passes into region-wide **events** (within about 10 days). That means `flood_events.tif` with one band per event plus a `flood_events.json` sidecar, and the plot reports the events it was flooded in. Not adopted yet.
- **Orphan flooded passes** (no regional event): show them as "local/unconfirmed" or drop them as noise. The dry-date test decides.
- **Score format:** decided after customer interviews.

## Skipped until needed
PostGIS, accounts, payments, cadastral ID lookup, more regions, ML. ML is a stretch goal only if everything else is finished.

**Cut first if time runs short:**
1. map overlays of the layers
2. TiTiler
3. the sub-scores display
