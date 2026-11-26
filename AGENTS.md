# Notes for AI assistants (and new teammates)

Read `docs/architecture.md` before changing anything: it records what the team agreed and why.

## Commands
- `uv sync`: install the exact locked dependencies (Python 3.14)
- `uv run fastapi dev api/main.py`: run the API, docs at http://127.0.0.1:8000/docs
- The API needs `hand.tif`, `flood_gfm.tif` and `ground.tif` in `data/processed/`: copy them from the team Drive, or build them with `pipeline/hand.py`, `pipeline/flood_gfm.py` and `pipeline/ground.py` (EGMS login, manual download)
- `uv run pytest`: tests
- `uv run python pipeline/flood_earthengine.py --help`: fallback flood pipeline (needs `earthengine authenticate` and `GEE_PROJECT`)

## Rules
- **Dependencies:** add them with `uv add`, never pip. Commit `uv.lock`.
- **The evidence contract** is the Pydantic models in `api/main.py`. Don't change its shape without saying so explicitly, because the frontend depends on it.
- **Missing data stays `unknown`.** Never default it to a low-risk value.
- **Never commit:**
  - secrets (`gee-key.json`, `*-key.json`, `.env`)
  - data files outside `data/sample/`
  - anything from AIM-Space
- **Keep it minimal:**
  - no speculative scaffolding, abstractions or stub folders
  - flood thresholds live as constants in `pipeline/flood_earthengine.py`; bump `ALGORITHM_VERSION` when you change them
- **Docs:** if you change a decision, update `docs/architecture.md` in the same commit.
- **`flood_gfm.tif` has no COG overviews** (since 26 Nov 2026): the overview step made the 10-year build hang. If you add TiTiler or a map of the flood layer, read the revert steps in `docs/architecture.md` ("Why these choices", COG) first.
