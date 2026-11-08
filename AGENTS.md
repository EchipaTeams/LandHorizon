# Notes for AI assistants (and new teammates)

Read `docs/architecture.md` before changing anything: it records what the team agreed and why.

## Commands
- `uv sync`: install the exact locked dependencies (Python 3.14)
- `uv run fastapi dev api/main.py`: run the API, docs at http://127.0.0.1:8000/docs
- `uv run python pipeline/hand.py`: build `data/processed/hand.tif` (needed by the API)
- `uv run pytest`: tests
- `uv run python pipeline/flood.py --help`: flood pipeline (needs `earthengine authenticate` and `GEE_PROJECT`)

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
  - flood thresholds live as constants in `pipeline/flood.py`; bump `ALGORITHM_VERSION` when you change them
- **Docs:** if you change a decision, update `docs/architecture.md` in the same commit.
