# check_gfm.py — run: uv run --with pystac-client python check_gfm.py
import numpy as np, rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from pystac_client import Client

PECHEA = (27.70, 45.58, 27.90, 45.68)  # lon/lat box around Pechea; adjust if off
items = Client.open("https://stac.eodc.eu/api/v1").search(
    collections="GFM", bbox=PECHEA, datetime="2024-09-12/2024-09-20").items()
for it in sorted(items, key=lambda i: i.datetime):
    for name in ("ensemble_flood_extent", "exclusion_mask"):
        with rasterio.open(it.assets[name].href) as src:
            win = from_bounds(*transform_bounds("EPSG:4326", src.crs, *PECHEA), src.transform)
            vals, counts = np.unique(src.read(1, window=win, boundless=True, fill_value=255), return_counts=True)
        print(it.datetime, name, dict(zip(vals.tolist(), counts.tolist())))