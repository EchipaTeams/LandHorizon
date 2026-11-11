# LandHorizon

Draw a land plot on a map and see what satellites measured there: flood history (Sentinel-1), ground motion (EGMS) and terrain height above the nearest river (HAND). Missing data is reported as unknown, never as low risk.

How it's built and why: [docs/architecture.md](docs/architecture.md).

## Layout
```
api/        backend: the evidence contract + POST /evidence (terrain real, rest mock)
pipeline/   batch jobs that turn satellite data into COGs (flood, HAND)
web/        frontend: React + MapLibre (frontend team, not set up yet)
docs/       architecture and decisions
```
Full tree: [docs/architecture.md](docs/architecture.md#repository-layout).

## Run it
Needs Python 3.14 and [uv](https://docs.astral.sh/uv/).

```
uv sync
uv run python pipeline/hand.py      # once: builds data/processed/hand.tif (~20 MB, public data)
uv run python pipeline/flood_gfm.py 2024-01-01 2025-01-01   # once: data/processed/flood_gfm.tif (public data, no account, ~1 h)
uv run fastapi dev api/main.py      # API docs at http://127.0.0.1:8000/docs
uv run pytest                       # tests
```

Flood validation: score GFM against a Copernicus EMS outline (zips in `data/raw/reference/`, gitignored) or on a no-flood window:
```
uv run python pipeline/gfm_score.py 2024-09-12 2024-09-25 --reference data/raw/reference/EMSR758_AOI03_DEL_PRODUCT_v1.zip
uv run python pipeline/gfm_score.py 2023-09-12 2023-09-25
```

Fallback flood pipelines (our own method; see [docs/architecture.md](docs/architecture.md#flood-method)). Earth Engine needs an account with a Cloud project:
```
uv run earthengine authenticate
export GEE_PROJECT=<cloud-project-id>          # PowerShell: $env:GEE_PROJECT = "<cloud-project-id>"
uv run python pipeline/flood.py --orbits 2024-09-01 2024-10-01
```

Local flood pipeline (prototype, no Earth Engine). It needs [ESA SNAP](https://step.esa.int/main/download/snap-download/) and a free [Copernicus Data Space](https://dataspace.copernicus.eu) account. Each scene downloads about 1.7 GB, which is deleted after processing; the first event run fetches about 34 scenes.
```
# .env (gitignored):  CDSE_USER=...  CDSE_PASSWORD=...   optional: SNAP_GPT=/path/to/gpt
set -a; source .env; set +a
uv run python pipeline/flood_local.py --event 2024-09-12 2024-09-25
```

Contains modified Copernicus Sentinel data, processed with ESA SNAP, and modified Copernicus Emergency Management Service information (GFM).