"""LandHorizon API.

/evidence returns, for the plot: real terrain (HAND), real flood history (Copernicus GFM) with the cropland
share of its flagged pixels (ESA WorldCover), real ground motion (EGMS) and the plot's real size. overall is
still a fixed mock: its format waits for the customer interviews.
"""
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated, Literal

import numpy as np
import rasterio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rasterio.features import bounds
from rasterio.mask import raster_geometry_mask
from rasterio.warp import transform_geom

app = FastAPI(title="LandHorizon API", version="0.1")
PROCESSED = Path(__file__).resolve().parents[1] / "data" / "processed"
HAND_PATH = Path(os.environ.get("HAND_PATH", PROCESSED / "hand.tif"))
FLOOD_PATH = Path(os.environ.get("FLOOD_PATH", PROCESSED / "flood_gfm.tif"))  # from pipeline/flood_gfm.py
GROUND_PATH = Path(os.environ.get("GROUND_PATH", PROCESSED / "ground.tif"))  # from pipeline/ground.py
WORLDCOVER_PATH = Path(os.environ.get("WORLDCOVER_PATH", PROCESSED / "worldcover.tif"))  # from pipeline/worldcover.py
CROPLAND = 40  # ESA WorldCover class code for cropland
# A pass counts as a flood date for the plot when it saw water on at least this share of the plot's
# observed pixels. Needs review: it keeps one stray wet pixel from becoming a "flood".
FLOOD_DATE_MIN_SHARE = 0.05
# Below this share of the plot observed, flood is "unknown": what a satellite saw on one corner doesn't
# describe the plot. Needs review: 0.5 is a judgment call, to be checked on the 20 test plots.
MIN_OBSERVED_FRACTION = 0.5
# Below this share of the plot's pixels with HAND data, terrain is "unknown": a median from one corner doesn't
# describe the plot. 0.5 mirrors MIN_OBSERVED_FRACTION; accepted by the lead on 21 Nov 2026.
TERRAIN_MIN_SHARE = 0.5
# Below this share of the cells whose centre is inside the plot with EGMS data, ground is "unknown": one cell doesn't
# describe a plot that holds several. Needs review: 0.5 mirrors the two above, the lead decides (L3).
GROUND_MIN_SHARE = 0.5

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
    cropland_share: float | None     # share of the flagged pixels that WorldCover maps as cropland; None when not computed
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
                flooded_fraction=0.42, cropland_share=0.6, algorithm_version="0.1",
                period_start=date(2024, 1, 1), period_end=date(2024, 12, 31)),
    ground=Ground(status="unknown", velocity_mm_yr=None, n_cells=0, release="2019-2023"),
    terrain=Terrain(status="measured", hand_m=1.7),
    # Fixed for every plot, so its reason must not claim anything about the plot's layers.
    overall=Overall(status="incomplete", score=None,
                    reasons=["no overall score yet: its format waits for the customer interviews"]),
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
        # mask() only fails when the plot misses the raster entirely; a plot across its edge would be answered
        # from the part inside, and nothing would say so. Each layer is a rectangle in its own CRS, so comparing
        # the plot's bounds with the raster's is exact.
        left, bottom, right, top = bounds(geom)
        b = src.bounds
        if left < b.left or bottom < b.bottom or right > b.right or top > b.top:
            raise HTTPException(422, f"Plot is partly or fully outside the covered area ({path.name}); "
                                     f"draw it inside the area of interest.")
        # Only pixels outside the plot are masked, not filled with 0 (0 is a real value). Unlike mask(), no-data
        # pixels inside the plot stay unmasked (NaN), so a layer can tell how much of the plot has data.
        outside, _, window = raster_geometry_mask(src, [geom], crop=True, all_touched=all_touched)
        data = src.read(window=window)
        return np.ma.masked_array(data, np.broadcast_to(outside, data.shape).copy()), src.descriptions, src.tags()


def cropland_share(polygon: Polygon, flagged) -> float | None:
    """Share of the flagged pixels (on the flood grid) that WorldCover maps as cropland, where GFM's spring false
    alarm on tilled fields happens. A caveat, not a verdict: it doesn't say a flood date is false.
    None when no pixel is flagged or WorldCover has no data on them, never 0."""
    cover, _, _ = read_plot(WORLDCOVER_PATH, polygon, "run pipeline/worldcover.py")
    with rasterio.open(WORLDCOVER_PATH) as c, rasterio.open(FLOOD_PATH) as f:
        same_grid = (c.crs, c.transform, c.shape) == (f.crs, f.transform, f.shape)
    if not same_grid:  # worldcover.tif must be pixel for pixel on the grid of flood_gfm.tif
        raise HTTPException(503, f"{WORLDCOVER_PATH.name} is not on the grid of {FLOOD_PATH.name}; rebuild it with "
                                 f"pipeline/worldcover.py")
    codes = cover[0].filled(0)[flagged]  # 0 = no data
    codes = codes[codes > 0]
    return round(float((codes == CROPLAND).mean()), 3) if codes.size else None


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
    flagged = seen & (n_flooded.filled(0) > 0)  # the pixels flooded_fraction counts
    # Read first, so a missing layer is a 503 whatever the plot (a broken server, not missing data).
    cropland = cropland_share(polygon, flagged)
    if observed < MIN_OBSERVED_FRACTION:  # GFM excluded (most of) the plot: high ground, city, forest, radar shadow
        return Flood(status="unknown", flood_dates=[], flooded_fraction=None, cropland_share=None, **behind)
    dates = sorted({date.fromisoformat(name[:10]) for name, band in zip(names[2:], data[2:])
                    if band.filled(0)[seen].mean() >= FLOOD_DATE_MIN_SHARE})
    return Flood(status="measured", flood_dates=dates,
                 flooded_fraction=round(float((n_flooded.filled(0)[seen] > 0).mean()), 3),
                 cropland_share=cropland, **behind)


def terrain(polygon: Polygon) -> Terrain:
    """Median HAND under the plot. Less than TERRAIN_MIN_SHARE of the plot with data -> unknown, never a guess."""
    data, _, _ = read_plot(HAND_PATH, polygon, "run pipeline/hand.py")
    inside = data.compressed()  # the plot's pixels
    values = inside[~np.isnan(inside)]
    if values.size == 0 or values.size / inside.size < TERRAIN_MIN_SHARE:
        return Terrain(status="unknown", hand_m=None)
    return Terrain(status="measured", hand_m=round(float(np.median(values)), 1))


def ground(polygon: Polygon) -> Ground:
    """Median EGMS vertical velocity of the cells whose centre is inside the plot.

    The same rule as pipeline/ground.py --plots. Counting every 100 m cell a plot merely touches would
    give a 0.5 ha plot the motion of a building next to it. Less than GROUND_MIN_SHARE of those cells with data
    (or no cell at all) -> unknown, never 0.
    """
    data, _, tags = read_plot(GROUND_PATH, polygon, "run pipeline/ground.py", all_touched=False)
    inside = data.compressed()  # the cells whose centre is inside the plot; NaN where EGMS has no cell
    values = inside[~np.isnan(inside)]
    release = tags["RELEASE"]  # written by ground.py from the EGMS file names, e.g. "2020-2025"
    # n_cells counts the cells with data either way, so an "unknown" can say how much data sits behind it.
    if values.size == 0 or values.size / inside.size < GROUND_MIN_SHARE:
        return Ground(status="unknown", velocity_mm_yr=None, n_cells=int(values.size), release=release)
    return Ground(status="measured", velocity_mm_yr=round(float(np.median(values)), 1),
                  n_cells=int(values.size), release=release)


def ring_area(ring) -> float:
    """Shoelace area of one ring, in the units of its coordinates squared."""
    x, y = np.array(ring, dtype=float).T
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2


def plot(polygon: Polygon) -> Plot:
    """The plot's size: its area, and how many pixels of the flood grid it covers.

    Call it after flood(), which answers 503 / 422 when the flood layer is missing or the plot isn't fully inside it.
    """
    # Area in ETRS89-LAEA (EPSG:3035), an equal-area projection, as pipeline/ground.py does. Holes are subtracted.
    outer, *holes = transform_geom("EPSG:4326", "EPSG:3035", polygon.model_dump())["coordinates"]
    area_m2 = ring_area(outer) - sum(ring_area(h) for h in holes)
    # n_pixels (reading accepted by the lead, 19 Nov 2026): the pixels of the flood grid (10 m) the plot
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
