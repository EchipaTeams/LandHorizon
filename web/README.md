# LandHorizon Web (`web/`)

Frontend UI/UX for LandHorizon: draw or select a land plot on a map, inspect satellite-measured flood history (Sentinel-1 / Copernicus GFM), terrain height above nearest drainage (HAND), and ground motion (EGMS), and print a PDF evidence report.

**Where the code lives:** the website is built in [`EchipaTeams/demo-repository`](https://github.com/EchipaTeams/demo-repository) (private). This file records the frontend decisions for the backend team and the lead, and how the website talks to the API.

## Milestone 3 UI/UX Architecture Decisions

1. **React + TypeScript (Vite):**
   - The client types (`Polygon` request, `Evidence` response) are **generated** from the API's OpenAPI schema with [`openapi-typescript`](https://openapi-ts.dev/), never written by hand. The Pydantic models in [`api/main.py`](../api/main.py) stay the only copy of the contract ([architecture](../docs/architecture.md#the-evidence-contract)). When the contract changes, regenerating the types turns every place the website uses an old field into a TypeScript error. See *Generated files*.
   - Map rendering and polygon drawing powered by **MapLibre GL** (open-source, token-free) centered on the Galați pilot AOI (`[27.5, 45.35, 28.25, 45.85]`).

2. **Tailwind CSS:**
   - Utility-first styling for the split-screen map + evidence panel layout.
   - Dedicated `@media print` styles so the evidence view exports cleanly to PDF via the browser's native print dialog (`window.print()`).

3. **Sample Plot Picker (`data/sample/plots.geojson`):**
   - Alongside freehand polygon drawing on the map, the UI includes a quick selector to load any of the 20 test plots from [`data/sample/plots.geojson`](../data/sample/plots.geojson) (`flood_sept_2024`, `never_flooded`, `unknown`, `spring_false_alarm`, `probe`) for fast verification and demos.

4. **Mock mode: a manual toggle, never an automatic fallback:**
   - `MOCK` in `api/main.py` looks measured (flood `measured`, 42 % flooded, HAND 1.7 m). If the UI switched to it by itself when the API failed, users would read fake data as real, which breaks the `unknown` rule.
   - Only a developer turns mock mode on, by hand. While it is on, every view, including the printed PDF, shows a visible **MOCK** label.
   - With mock mode off, an API error is shown as an error. A **503** (the server is missing one of its COGs) says the server isn't ready. It never shows mock data and never says `unknown`: `unknown` means the satellites didn't see the plot, not that the server is broken.
   - The mock JSON is not hand-written: it is exported from `MOCK` (see *Generated files*).

## Product Rules Enforced in the UI

- **The `unknown` rule:** Any layer with `status: "unknown"` (or `null` metrics such as `flooded_fraction: null`, `hand_m: null`, `velocity_mm_yr: null`) is explicitly badged and explained as **Unknown** (together with `observed_fraction` and `terrain.hand_m`), **never** displayed as "Low risk" or `0%`.
- **Single source of truth:** The UI consumes `POST /evidence` directly without redefining or altering the backend contract shape. The types and the mock JSON are generated from the backend, never written by hand.

## Generated files

The website generates two files from this repo instead of keeping hand-written copies. Don't edit them by hand. Regenerate them whenever `api/main.py` changes.

**Types**, with the API running (see below), from the website repo:
```bash
npx openapi-typescript http://127.0.0.1:8000/openapi.json -o src/api/schema.d.ts
```

**Mock JSON**, from the root of this repo (no COGs needed), written into the website repo:
```bash
uv run python -c "from api.main import MOCK; print(MOCK.model_dump_json(indent=2))" > ../demo-repository/src/api/mock.json
```
(Adjust `../demo-repository` to wherever the website repo is cloned.)

## Running Locally

### 1. Start the Backend API
From the root of this repo:
```bash
uv sync
uv run fastapi dev api/main.py
```
The API runs at `http://127.0.0.1:8000` (OpenAPI docs at `http://127.0.0.1:8000/docs`). `POST /evidence` answers **503** until `hand.tif`, `flood_gfm.tif` and `ground.tif` are in `data/processed/` (copy them from the team Drive). Until then the website shows that error, or a developer turns mock mode on by hand.

### 2. Start the Frontend Dev Server
From the website repo (`EchipaTeams/demo-repository`):
```bash
npm install
npm run dev
```
The Vite dev server runs at `http://localhost:5173` and proxies `/evidence` requests to `http://127.0.0.1:8000`.
