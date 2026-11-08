"""LandHorizon API.

For now /evidence returns a fixed mock, so the frontend can build against
the contract before any real data exists.
"""
from datetime import date
from typing import Annotated, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="LandHorizon API", version="0.1")

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


@app.post("/evidence")
def evidence(polygon: Polygon) -> Evidence:
    # TODO: replace with rasterio.mask over the COGs
    return MOCK
