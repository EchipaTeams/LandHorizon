"""LandHorizon API.

/evidence returns, for the plot: real terrain (HAND), real flood history (Copernicus GFM), real
ground motion (EGMS) and the plot's real size. overall is still a fixed mock: its format waits
for the customer interviews.
"""
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated, Literal

import numpy as np
import rasterio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rasterio.mask import mask, raster_geometry_mask
from rasterio.warp import transform_geom

app = FastAPI(title="LandHorizon API", version="0.1")
PROCESSED = Path(__file__).resolve().parents[1] / "data" / "processed"
HAND_PATH = Path(os.environ.get("HAND_PATH", PROCESSED / "hand.tif"))
FLOOD_PATH = Path(os.environ.get("FLOOD_PATH", PROCESSED / "flood_gfm.tif"))  # from pipeline/flood_gfm.py
GROUND_PATH = Path(os.environ.get("GROUND_PATH", PROCESSED / "ground.tif"))  # from pipeline/ground.py
# A pass counts as a flood date for the plot when it saw water on at least this share of the plot's
# observed pixels. Needs review: it keeps one stray wet pixel from becoming a "flood".
FLOOD_DATE_MIN_SHARE = 0.05
# Below this share of the plot observed, flood is "unknown": what a satellite saw on one corner doesn't
# describe the plot. Needs review: 0.5 is a judgment call, to be checked on the 20 test plots.
MIN_OBSERVED_FRACTION = 0.5

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
    status: Status                   # unknown when observed_fraction is under MIN_OBSERVED_FRACTION
    observed_fraction: float         # share of the plot's pixels that at least one pass could see (0 to 1)
    flood_dates: list[date]          # days a satellite pass saw water on the plot (see FLOOD_DATE_MIN_SHARE)
    n_passes: int                    # typical number of passes that observed each observed pixel of the plot
    flooded_fraction: float | None   # share of the observed plot ever seen flooded; None when unknown
    algorithm_version: str
    period_start: date               # first day of the flood history (inclusive)
    period_end: date                 # last day of the flood history (inclusive)


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
    flood=Flood(status="measured", observed_fraction=1.0, flood_dates=[date(2024, 9, 15)], n_passes=212,
                flooded_fraction=0.42, algorithm_version="0.1",
                period_start=date(2024, 1, 1), period_end=date(2024, 12, 31)),
    ground=Ground(status="unknown", velocity_mm_yr=None, n_cells=0, release="2019-2023"),
    terrain=Terrain(status="measured", hand_m=1.7),
    overall=Overall(status="incomplete", score=None, reasons=["no ground-motion cells under plot"]),
)


def read_plot(path: Path, polygon: Polygon, missing_hint: str, all_touched: bool = True):
    """The raster's pixels under the plot as a masked array (bands, rows, cols), its band descriptions and tags.

    all_touched=True: a small plot still gets every pixel it touches (right for the 10-30 m layers).
    all_touched=False: a pixel counts only if its centre is inside the plot (the rule for the 100 m EGMS cells).
    """
    if not path.exists():  # a broken server, not a satellite gap: fail loudly instead of saying "unknown"
        raise HTTPException(503, f"Layer missing at {path}; {missing_hint}")
    with rasterio.open(path) as src:
        geom = transform_geom("EPSG:4326", src.crs, polygon.model_dump())
        try:
            # filled=False: pixels outside the plot come back masked, not as 0 (0 is a real value).
            data, _ = mask(src, [geom], crop=True, all_touched=all_touched, filled=False)
        except ValueError as e:
            if "do not overlap" not in str(e):
                raise
            raise HTTPException(422, "Plot is outside the covered area.") from e
        return data, src.descriptions, src.tags()


def flood(polygon: Polygon) -> Flood:
    """Flood history under the plot from GFM. Barely or never observed -> unknown, never "not flooded"."""
    data, names, tags = read_plot(FLOOD_PATH, polygon, "run pipeline/flood_gfm.py")
    # flood_gfm.py writes the build period with an exclusive end (2025-01-01); report it inclusive.
    period = dict(period_start=date.fromisoformat(tags["period_start"]),
                  period_end=date.fromisoformat(tags["period_end"]) - timedelta(days=1))
    n_flooded, n_passes = data[0], data[1]
    inside = ~np.ma.getmaskarray(n_passes)  # the plot's pixels
    seen = inside & (n_passes.filled(0) > 0)
    observed = seen.sum() / max(inside.sum(), 1)
    # How much data sits behind the answer is reported either way, so "unknown" can say why.
    behind = dict(observed_fraction=round(float(observed), 3),
                  n_passes=int(np.median(n_passes.filled(0)[seen])) if seen.any() else 0,
                  algorithm_version="gfm-ensemble", **period)
    if observed < MIN_OBSERVED_FRACTION:  # GFM excluded (most of) the plot: high ground, city, forest, radar shadow
        return Flood(status="unknown", flood_dates=[], flooded_fraction=None, **behind)
    dates = sorted({date.fromisoformat(name[:10]) for name, band in zip(names[2:], data[2:])
                    if band.filled(0)[seen].mean() >= FLOOD_DATE_MIN_SHARE})
    return Flood(status="measured", flood_dates=dates,
                 flooded_fraction=round(float((n_flooded.filled(0)[seen] > 0).mean()), 3), **behind)


def terrain(polygon: Polygon) -> Terrain:
    """Median HAND under the plot. No pixels with data -> unknown, never a guess."""
    data, _, _ = read_plot(HAND_PATH, polygon, "run pipeline/hand.py")
    values = data.compressed()
    values = values[~np.isnan(values)]
    if values.size == 0:
        return Terrain(status="unknown", hand_m=None)
    return Terrain(status="measured", hand_m=round(float(np.median(values)), 1))


def ground(polygon: Polygon) -> Ground:
    """Median EGMS vertical velocity of the cells whose centre is inside the plot. No cell -> unknown, never 0.

    The same rule as pipeline/ground.py --plots. Counting every 100 m cell a plot merely touches would
    give a 0.5 ha plot the motion of a building next to it.
    """
    data, _, tags = read_plot(GROUND_PATH, polygon, "run pipeline/ground.py", all_touched=False)
    values = data.compressed()
    values = values[~np.isnan(values)]
    release = tags["RELEASE"]  # written by ground.py from the EGMS file names, e.g. "2020-2025"
    if values.size == 0:
        return Ground(status="unknown", velocity_mm_yr=None, n_cells=0, release=release)
    return Ground(status="measured", velocity_mm_yr=round(float(np.median(values)), 1),
                  n_cells=int(values.size), release=release)


def ring_area(ring) -> float:
    """Shoelace area of one ring, in the units of its coordinates squared."""
    x, y = np.array(ring, dtype=float).T
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2


def plot(polygon: Polygon) -> Plot:
    """The plot's size: its area, and how many pixels of the flood grid it covers.

    Call it after flood(), which answers 503 / 422 when the flood layer is missing or the plot is outside it.
    """
    # Area in ETRS89-LAEA (EPSG:3035), an equal-area projection, as pipeline/ground.py does. Holes are subtracted.
    outer, *holes = transform_geom("EPSG:4326", "EPSG:3035", polygon.model_dump())["coordinates"]
    area_m2 = ring_area(outer) - sum(ring_area(h) for h in holes)
    # n_pixels, proposed reading (needs the lead's review): the pixels of the flood grid (10 m) the plot
    # touches. These are the pixels flood.observed_fraction is a share of. Only the grid is used, no pixel is read.
    with rasterio.open(FLOOD_PATH) as src:
        outside, _, _ = raster_geometry_mask(src, [transform_geom("EPSG:4326", src.crs, polygon.model_dump())],
                                             crop=True, all_touched=True)
    return Plot(area_ha=round(area_m2 / 10_000, 2), n_pixels=int((~outside).sum()))


@app.post("/evidence")
def evidence(polygon: Polygon) -> Evidence:
    # Everything is read under the plot except overall, which is still the mock.
    layers = {"terrain": terrain(polygon), "flood": flood(polygon), "ground": ground(polygon)}
    return MOCK.model_copy(update={**layers, "plot": plot(polygon)})
