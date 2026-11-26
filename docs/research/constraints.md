# Research constraints

What any proposed improvement has to fit. Collected on 11 Nov 2026 from `docs/architecture.md`, `AGENTS.md` and the team's project plan. Figures marked *(course notes)* come from the masterclass material and were not rechecked: verify them before a recommendation depends on one.

## Time and people
- **Final submission 11 Dec 2026**, to be ready the evening of 10 Dec. **Feature freeze Sun 6 Dec.**
- Milestones: data test 15 Nov, real slice + gate 22 Nov, flood validated 29 Nov.
- Team of 7 students at about 8–10 h/week each: roughly 280–350 person-hours **for the whole project**, business work included. About 2 people on flood, 1–2 on ground.
- Every team member must be able to explain the data, method, code and results. A method nobody on the team can explain is not usable, however accurate.

## Scope
- Enterprise Software track: a working web platform. The submission must **separate what is implemented from future development**, so a well-argued roadmap item has real value in the pitch even if it isn't built.
- One pilot region (Galați, provisional). National coverage is a pitch line, not a deliverable.
- Plots are small: under 1 ha, 1–5 ha, and larger. A data source much coarser than a plot describes the region, not the plot, and must be presented that way.
- **A new hazard or a new sensor is rated "expensive, out of scope after the 22 Nov gate"** in the plan. Heatwave/drought is a new hazard, so the default expectation is a roadmap item unless something very cheap and honest exists.
- **No ML in the plan.** ML is a stretch goal only if everything else is finished. A simple, explainable baseline has to be beaten first.
- The product is a **screening indicator based on past observations and terrain, not a probability**. About 10 years of Sentinel-1 is too short for flood return periods, and the report must not claim them from our own data.

## Architecture
- Batch pipeline runs **ahead of time** and writes COGs. The API only reads the COG pixels under the drawn plot. Nothing heavy per request, no database, nothing stored per request.
- Python 3.14 with `uv`. A new dependency must install on 3.14 (check for wheels) and is added with `uv add`.
- The evidence contract (Pydantic models in `api/main.py`) changes only with the lead's review, because the frontend depends on it.
- Flood thresholds are constants in `pipeline/flood_earthengine.py`; changing them bumps `ALGORITHM_VERSION`.

## Data and money
- **Free and openly licensed data only.** Check the licence allows use in a product, not only research.
- **No AIM-Space data** anywhere in the product or the repo (course rule).
- No secrets and no data files in git outside `data/sample/`.
- Compute is free tiers only: Google Earth Engine 150 EECU-h/month, non-commercial (commercial use is paid); CDSE openEO 10,000 credits/month *(course notes)*; student cloud credits of about $100–300 *(course notes)*.
- Sources that need a manual login (like EGMS) can't be scripted and cost team time.

## Method rules
- **Missing data is `unknown`, never a low-risk value.** "No flood seen" is weak evidence, not proof of safety.
- Thresholds and pass criteria are written down **before** a test is run. A method is not changed silently to pass.
- Validate against a reference from an **independent sensor**, split by event, time or region (not randomly), and report precision and recall.
- State limits plainly: what was tested, what was observed, what that does not prove.

## Current state (see `docs/architecture.md` for detail)
- **Flood:** Copernicus GFM (Sentinel-1, 20 m), counted per pixel for 2024. It passes the September tests and **fails the spring dry-window test**: 9.06 % of land flagged against a 1 % limit, from freshly tilled fields on 30 Apr–1 May 2024. This is the open decision blocking the 2015–2025 batch. Our own thresholding method (v0.2) is kept as a fallback.
- **Terrain:** HAND from the Copernicus 30 m DEM, live.
- **Ground:** means **ground motion** here, not terrain. Not built. Planned: EGMS Ortho (100 m, vertical + east-west) rasterized once. Plots of 1 ha or less get 0–1 cells. 2 mm/year is treated as the noise floor; no source was found for a 5 mm/year threshold. The API returns a mock for now.
- **Heat/drought:** nothing exists.
- **Closest competitor:** Imoreview (free; uses EGMS and RO-FLOODS for buildings).
