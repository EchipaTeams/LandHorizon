# LandHorizon

Draw a land plot on a map and see what satellites measured there: flood history (Sentinel-1), ground motion (EGMS) and terrain height above the nearest river (HAND). Missing data is reported as unknown, never as low risk.

How it's built and why: [docs/architecture.md](docs/architecture.md).

## Layout
```
api/        FastAPI app: the evidence contract + POST /evidence (mock for now)
pipeline/   batch jobs that turn satellite data into COGs (flood.py: Sentinel-1 in Earth Engine)
docs/       architecture and decisions
```

## Run it
Needs Python 3.14 and [uv](https://docs.astral.sh/uv/).

```
uv sync
uv run python pipeline/hand.py      # once: builds data/processed/hand.tif (~20 MB, public data)
uv run fastapi dev api/main.py      # API docs at http://127.0.0.1:8000/docs
uv run pytest                       # tests
```

Flood pipeline (needs an Earth Engine account with a Cloud project):
```
uv run earthengine authenticate
$env:GEE_PROJECT = "<cloud-project-id>"
uv run python pipeline/flood.py --orbits 2024-09-01 2024-10-01
```