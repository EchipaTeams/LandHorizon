# Sending a plot: frontend ↔ backend

For the agents working on either side. The website (`EchipaTeams/demo-repository`) sends the plot the user drew, and the API (`api/main.py`) answers with what satellites measured there. This file covers only that exchange. The contract's fields are not repeated here: they live in the Pydantic models in `api/main.py` (browse them at `/docs`), and the website's types are generated from them ([web/README.md](../web/README.md#generated-files)).

## The request
`POST /evidence`, `Content-Type: application/json`. The body is a **GeoJSON Polygon geometry** and nothing else:

```json
{"type": "Polygon",
 "coordinates": [[[27.695819, 45.688913], [27.69659, 45.688909], [27.696601, 45.689809],
                  [27.69583, 45.689813], [27.695819, 45.688913]]]}
```

- **Only the geometry, never the Feature.** Send `feature.geometry`. A `Feature`, `FeatureCollection` or `MultiPolygon` gets a 422.
- **`[lon, lat]`, WGS84 (EPSG:4326)**, the order MapLibre uses. Swapped coordinates land outside the area and get a 422.
- **The ring is closed:** at least 4 points, the last equal to the first. Extra rings are holes; their area is subtracted.
- **One polygon per request.** The user draws one plot at a time.
- **The area of interest is Galați, `[27.5, 45.35, 28.25, 45.85]`** (west, south, east, north). The whole plot must be inside it.

## The responses
| Status | Meaning | The website shows |
|---|---|---|
| 200 | An `Evidence` JSON | The result. A layer with `status: "unknown"` (or a `null` value) is shown as **Unknown**, never as low risk or 0 % |
| 422 | Wrong body shape, or part of the plot is outside the covered area. `detail` says which | "Draw the plot inside the area of interest", or the validation message |
| 503 | A data layer (COG) is missing on the server | A server error. Never mock data, never "unknown": unknown means the satellites didn't see the plot |

## Frontend rules
- Call the API through the generated client types (`Polygon` request, `Evidence` response). Never hand-write them; regenerate after any change to `api/main.py`.
- Call `/evidence` by its relative path. In development the Vite server proxies it to `http://127.0.0.1:8000`; when deployed, see *Deployment* below.
- Block self-intersecting polygons (a "bow tie") before sending. The backend doesn't check for them, and its area and pixel counts would be wrong.
- Mock mode is a manual developer toggle, never a fallback when a request fails. While it is on, every view and the printed PDF show a **MOCK** label.

```ts
const res = await fetch("/evidence", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(feature.geometry),
});
if (res.status === 422) { /* plot outside the area, or a bad shape: show detail */ }
else if (res.status === 503) { /* server not ready: show as an error */ }
else if (res.ok) { const evidence: Evidence = await res.json(); /* render */ }
```

## Backend rules
- The request and response shapes are the `Polygon` and `Evidence` models in `api/main.py`. Changing either is a **contract change**: say so in the PR, get the lead's review, update [architecture.md](architecture.md#the-evidence-contract) in the same commit, and tell the frontend to regenerate its types.
- Missing data stays `unknown` with `null` values, never 0 or a low value.
- A missing COG answers 503, never "unknown". A plot not wholly inside every layer answers 422 with a message naming the layer.
- Keep the tests in `api/test_main.py` passing (`uv run pytest`); add one for every new rule.

## Deployment: not decided yet
The API has no CORS setting. Locally that works, because the browser only talks to the Vite server. Deployed on two different addresses, the browser will block the call. Two options:
- **One domain, with a reverse proxy** sending `/evidence` to the API (proposed). The frontend code above doesn't change, and the API stays closed to other sites.
- **CORS in FastAPI** (`CORSMiddleware`), allowing only the website's address.

The choice belongs to the deploy task. Until it is made, don't add a CORS setting that allows every origin (`*`).

**Proposed by the deploy task (G4, 28 Nov 2026, for the lead's review): one domain, with Caddy as the reverse proxy** (`Caddyfile`, `docker-compose.yml`). `/evidence`, `/docs` and `/openapi.json` go to the API; every other path serves the website's build output (`WEB_DIST`), with `index.html` for routes of the single-page app. No CORS setting is added, so the call above works unchanged. Caddy gets the HTTPS certificate for the domain by itself.
