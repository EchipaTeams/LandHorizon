# LandHorizon

Draw a land plot on a map and see what satellites measured there: flood history (Sentinel-1), ground motion (EGMS) and terrain height above the nearest river (HAND). Missing data is reported as unknown, never as low risk.

How it's built and why: [docs/architecture.md](docs/architecture.md).

## Layout
```
api/        backend: the evidence contract + POST /evidence (all layers real, overall score still mock)
pipeline/   batch jobs that turn satellite data into COGs (flood, HAND, ground motion)
web/        frontend: React + MapLibre (frontend team, not set up yet)
docs/       architecture and decisions
```
Full tree: [docs/architecture.md](docs/architecture.md#repository-layout).

## Run it
Needs Python 3.14 and [uv](https://docs.astral.sh/uv/).

The API reads four COGs from `data/processed/` and answers 503 while one is missing. The quickest way to get them is to copy `hand.tif`, `flood_gfm.tif`, `ground.tif` and `worldcover.tif` from the team Drive into `data/processed/` (ask the team for access). Or build them yourself:
```
uv run python pipeline/hand.py      # data/processed/hand.tif (~20 MB, public data)
uv run python pipeline/flood_gfm.py 2015-01-01 2025-05-01   # data/processed/flood_gfm.tif, 2015 – 13 Apr 2025 (public data, no account, ~1¼ h with 8 parallel reads, ~8 GB of memory: lower `WORKERS` in the script on a smaller machine)
uv run python pipeline/ground.py    # data/processed/ground.tif; needs the EGMS tiles in data/raw/egms/ (login, see the script)
uv run python pipeline/worldcover.py   # data/processed/worldcover.tif (~2 MB, public data, seconds); on the grid of flood_gfm.tif
```

Then:
```
uv sync
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
uv run python pipeline/flood_earthengine.py --orbits 2024-09-01 2024-10-01
```

Local flood pipeline (prototype, no Earth Engine). It needs [ESA SNAP](https://step.esa.int/main/download/snap-download/) and a free [Copernicus Data Space](https://dataspace.copernicus.eu) account. Each scene downloads about 1.7 GB, which is deleted after processing; the first event run fetches about 34 scenes.
```
# .env (gitignored):  CDSE_USER=...  CDSE_PASSWORD=...   optional: SNAP_GPT=/path/to/gpt
set -a; source .env; set +a
uv run python pipeline/flood_local.py --event 2024-09-12 2024-09-25
```

Contains modified Copernicus Sentinel data, processed with ESA SNAP, and modified Copernicus Emergency Management Service information (GFM). Permanent water: JRC Global Surface Water v1.4 (Pekel et al., 2016, Nature 540, 418–422, [doi:10.1038/nature20584](https://doi.org/10.1038/nature20584)). Source: EC JRC/Google. Land cover: © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium (CC BY 4.0).