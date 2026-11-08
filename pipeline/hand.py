"""Terrain: HAND (height above nearest drainage) for the AOI, as a local COG.

ASF's HAND tiles are COGs, so this reads only the AOI's window over HTTP
instead of downloading whole tiles, then writes data/processed/hand.tif.

  uv run python pipeline/hand.py
"""
import math
from pathlib import Path

import numpy as np
import rasterio
from rasterio.merge import merge

from flood import AOI

# ponytail: north/east hemispheres only, which covers Romania.
URL = "https://glo-30-hand.s3.us-west-2.amazonaws.com/v1/2021/Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_HAND.tif"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "hand.tif"


def main():
    lon0, lat0, lon1, lat1 = AOI
    urls = [URL.format(lat=lat, lon=lon)  # one tile per 1°x1° cell, named by its south-west corner
            for lat in range(math.floor(lat0), math.ceil(lat1))
            for lon in range(math.floor(lon0), math.ceil(lon1))]
    mosaic, transform = merge(urls, bounds=AOI, nodata=float("nan"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(OUT, "w", driver="COG", dtype="float32", count=1, crs="EPSG:4326",
                       width=mosaic.shape[2], height=mosaic.shape[1], transform=transform,
                       nodata=float("nan"), compress="deflate") as dst:
        dst.write(mosaic)

    band = mosaic[0]
    print(f"wrote {OUT} ({band.shape[1]}x{band.shape[0]} px) from {len(urls)} tiles; "
          f"HAND m: min {np.nanmin(band):.1f}, median {np.nanmedian(band):.1f}, "
          f"max {np.nanmax(band):.1f}, NaN {np.isnan(band).mean():.1%}")


if __name__ == "__main__":
    main()
