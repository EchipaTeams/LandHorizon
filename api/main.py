"""LandHorizon API.

For now /evidence returns a fixed mock, so the frontend can build against
the contract before any real data exists.
"""
import os
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

import numpy as np
import rasterio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rasterio.mask import mask
from rasterio.warp import transform_geom

app = FastAPI(title="LandHorizon API", version="0.1")
HAND_PATH = Path(os.environ.get("HAND_PATH", Path(__file__).resolve().parents[1] / "data" / "processed" / "hand.tif"))

Status = Literal["measured", "unknown"]
Ring = Annotated[list[tuple[float, float]], Field(min_length=4)]  # closed ring: first point == last


class Polygon(BaseModel):
    """GeoJSON Polygon, WGS84 lon/lat (what MapLibre draw gives you)."""
    type: Literal["Polygon"]
    coordinates: list[Ring]


class Plot(BaseModel):
    area_ha: float
    n_pixels: int


class Flood(BaseModel):
    status: Status
    flood_dates: list[date]
    n_passes: int
    flooded_fraction: float
    algorithm_version: str


class Ground(BaseModel):
    status: Status
    velocity_mm_yr: float | None
    n_cells: int
    release: str


class Terrain(BaseModel):
    status: Status
    hand_m: float | None


class Overall(BaseModel):
    status: str  # ponytail: free text until the scoring rules fix the set of values
    score: float | None
    reasons: list[str]


class Evidence(BaseModel):
    plot: Plot
    flood: Flood
    ground: Ground
    terrain: Terrain
    overall: Overall


MOCK = Evidence(
    plot=Plot(area_ha=0.8, n_pixels=80),
    flood=Flood(status="measured", flood_dates=[date(2024, 9, 15)], n_passes=212,
                flooded_fraction=0.42, algorithm_version="0.1"),
    ground=Ground(status="unknown", velocity_mm_yr=None, n_cells=0, release="2019-2023"),
    terrain=Terrain(status="measured", hand_m=1.7),
    overall=Overall(status="incomplete", score=None, reasons=["no ground-motion cells under plot"]),
)


def terrain(polygon: Polygon) -> Terrain:
    """Median HAND under the plot. No pixels with data -> unknown, never a guess."""
    if not HAND_PATH.exists():  # a broken server, not a satellite gap: fail loudly instead of saying "unknown"
        raise HTTPException(503, f"HAND layer missing at {HAND_PATH}; run pipeline/hand.py")
    with rasterio.open(HAND_PATH) as src:
        geom = transform_geom("EPSG:4326", src.crs, polygon.model_dump())
        try:
            # filled=False: pixels outside the plot come back masked, not as 0 (0 m is a real HAND value).
            # all_touched=True: a small plot still gets the ~30 m pixels it touches.
            data, _ = mask(src, [geom], crop=True, all_touched=True, filled=False)
        except ValueError as e:
            if "do not overlap" not in str(e):
                raise
            raise HTTPException(422, "Plot is outside the covered area.") from e
    values = data.compressed()
    values = values[~np.isnan(values)]
    if values.size == 0:
        return Terrain(status="unknown", hand_m=None)
    return Terrain(status="measured", hand_m=round(float(np.median(values)), 1))


@app.post("/evidence")
def evidence(polygon: Polygon) -> Evidence:
    # Terrain is real; plot, flood, ground and overall are still the mock.
    return MOCK.model_copy(update={"terrain": terrain(polygon)})
