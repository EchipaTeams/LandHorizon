# LandHorizon Web (`web/`)

Frontend UI/UX for LandHorizon: draw or select a land plot on a map, inspect satellite-measured flood history (Sentinel-1 / Copernicus GFM), terrain height above nearest drainage (HAND), and ground motion (EGMS), and print a PDF evidence report.

## Milestone 3 UI/UX Architecture Decisions

1. **React + TypeScript (Vite):**
   - Strictly typed client interfaces matching the Pydantic evidence contract in [`api/main.py`](../api/main.py) (`Polygon` request and `Evidence` response).
   - Map rendering and polygon drawing powered by **MapLibre GL** (open-source, token-free) centered on the Galați pilot AOI (`[27.5, 45.35, 28.25, 45.85]`).

2. **Tailwind CSS:**
   - Utility-first styling for the split-screen map + evidence panel layout.
   - Dedicated `@media print` styles so the evidence view exports cleanly to PDF via the browser's native print dialog (`window.print()`).

3. **Sample Plot Picker (`data/sample/plots.geojson`):**
   - Alongside freehand polygon drawing on the map, the UI includes a quick selector to load any of the 20 test plots from [`data/sample/plots.geojson`](../data/sample/plots.geojson) (`flood_sept_2024`, `never_flooded`, `unknown`, `spring_false_alarm`, `probe`) for fast verification and demos.

4. **Mock Mode Toggle:**
   - Includes a toggle (and fallback) to use the contract `MOCK` response when local COG rasters (`data/processed/hand.tif` and `data/processed/flood_gfm.tif`) have not been generated yet, allowing frontend development and testing independently of heavy raster pipelines.

## Product Rules Enforced in the UI

- **The `unknown` rule:** Any layer with `status: "unknown"` (or `null` metrics such as `flooded_fraction: null`, `hand_m: null`, `velocity_mm_yr: null`) is explicitly badged and explained as **Unknown** (together with `observed_fraction` and `terrain.hand_m`), **never** displayed as "Low risk" or `0%`.
- **Single source of truth:** The UI consumes `POST /evidence` directly without redefining or altering the backend contract shape.

## Running Locally (Once Scaffolding Is Added)

### 1. Start the Backend API (optional if using Mock Mode)
From the repository root:
```bash
uv sync
uv run fastapi dev api/main.py
```
The API runs at `http://127.0.0.1:8000` (OpenAPI docs at `http://127.0.0.1:8000/docs`).

### 2. Start the Frontend Dev Server
From the `web/` directory:
```bash
cd web
npm install
npm run dev
```
The Vite dev server runs at `http://localhost:5173` and proxies `/evidence` requests to `http://127.0.0.1:8000`.
