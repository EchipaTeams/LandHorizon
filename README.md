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
uv run fastapi dev api/main.py      # API docs at http://127.0.0.1:8000/docs
uv run pytest                       # tests
```

Flood pipeline (needs an Earth Engine account with a Cloud project):
```
uv run earthengine authenticate
$env:GEE_PROJECT = "<cloud-project-id>"
uv run python pipeline/flood.py --orbits 2024-09-01 2024-10-01
```