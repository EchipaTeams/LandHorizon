"""Land cover: ESA WorldCover 2021 cut to the flood grid, as a local COG.

The API uses it to say how much of the area the satellites flagged on a plot is cropland, where GFM's
spring false alarm on tilled fields happens (docs/flood-validation.md). Reads only the AOI's window over HTTP
from the one 3°x3° tile that holds the Galați AOI, then writes data/processed/worldcover.tif:

  uv run python pipeline/worldcover.py

The output is on exactly the grid of flood_gfm.tif (flood_common.grid(): UTM 35N, 10 m), nearest neighbour,
so a pixel of it is a pixel of flood_gfm.tif. Values are WorldCover's class codes (40 = cropland); 0 = no data.
Data: ESA WorldCover 2021 v200, CC BY 4.0, © ESA WorldCover project 2021 / Contains modified Copernicus
Sentinel data (2021) processed by ESA WorldCover consortium. Never commit it.
"""
from pathlib import Path

import numpy as np
import rasterio

import flood_common

# Same tile as checks/cropland_share/cropland_share.py, which did the cut for the decision check.
URL = ("https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
       "ESA_WorldCover_10m_2021_v200_N45E027_Map.tif")
OUT = flood_common.OUT / "worldcover.tif"


def cut(src) -> np.ndarray:
    """The class codes of an open WorldCover raster on the flood grid (uint8, 0 = no data)."""
    return np.nan_to_num(flood_common.to_grid(src), nan=0).astype("uint8")


def main():
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"), rasterio.open(URL) as src:
        cover = cut(src)
    transform, width, height = flood_common.grid()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(OUT, "w", driver="COG", dtype="uint8", count=1, crs=flood_common.CRS, width=width,
                       height=height, transform=transform, nodata=0, compress="deflate",
                       overview_resampling="nearest") as dst:  # nearest: class codes must not be averaged
        dst.write(cover, 1)
        dst.update_tags(source="ESA WorldCover 2021 v200", licence="CC BY 4.0")
    labelled = cover > 0
    print(f"wrote {OUT} ({width}x{height} px); no data {1 - labelled.mean():.1%}, "
          f"cropland (40) {(cover == 40).sum() / max(labelled.sum(), 1):.1%} of the pixels with data")


if __name__ == "__main__":
    main()
