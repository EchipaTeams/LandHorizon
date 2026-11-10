"""Ground motion: EGMS L3 vertical velocity (U) for the AOI, as a local COG.

EGMS needs a login, so download the L3 Ortho 'U' tiles covering the AOI by hand
into data/raw/ (the AOI spans two 100 km tiles), then:

  uv run python pipeline/ground.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import transform_bounds

from flood import AOI

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "ground.tif"
NAME = re.compile(r"EGMS_L3_(E\d+N\d+)_100km_U_(\d{4})_(\d{4})_\d+\.tiff?")  # not .aux.xml sidecars


def main():
    tiles = {m[1]: (p, f"{m[2]}-{m[3]}") for p in RAW.iterdir() if (m := NAME.fullmatch(p.name))}

    # The AOI in the EGMS grid (EPSG:3035). A tile is named by its lower-left corner in 100 km units:
    # E57N26 = x 5,700,000 / y 2,600,000. A tile left out would silently turn into "unknown", so insist on all.
    x0, y0, x1, y1 = bounds = transform_bounds("EPSG:4326", "EPSG:3035", *AOI)
    need = {f"E{ix}N{iy}" for ix in range(int(x0 // 1e5), int(x1 // 1e5) + 1)
            for iy in range(int(y0 // 1e5), int(y1 // 1e5) + 1)}
    
    if missing := need - tiles.keys():
        sys.exit(f"Missing EGMS tiles for the AOI: {sorted(missing)}. Download them into {RAW}.")
        
    paths = [tiles[t][0] for t in sorted(need)]
    
    if len(releases := {tiles[t][1] for t in need}) != 1:
        sys.exit(f"Tiles come from different releases: {sorted(releases)}")
    release = releases.pop()

    kinds = set()
    for p in paths:
        with rasterio.open(p) as src:
            kinds.add((src.crs.to_epsg(), src.dtypes[0], str(src.nodata), src.res))
            
    if len(kinds) != 1:
        sys.exit(f"Tiles disagree on CRS / dtype / nodata / resolution: {kinds}")
        
    (epsg, dtype, _, res), = kinds
    
    with rasterio.open(paths[0]) as src:
        nodata = src.nodata
        
    print(f"{len(paths)} tiles {sorted(need)}, release {release}, EPSG:{epsg}, {dtype}, nodata={nodata}, res={res}")
    
    if epsg != 3035 or nodata is None:
        sys.exit("Expected EPSG:3035 with a nodata value; refusing to guess, or empty cells could become 0 mm/yr.")

    # merge() with masked=True handles NaN/sentinel branches natively and returns a masked array.
    mosaic, transform = merge(paths, bounds=bounds, masked=True)  
    v = mosaic.compressed() # Extracts only the valid cells into a 1D arra
    
    if v.size == 0:
        sys.exit("No EGMS cells inside the AOI: check the tiles and the AOI.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the masked array back. Masked cells are written as nodata automatically.
    with rasterio.open(OUT, "w", driver="COG", dtype=mosaic.dtype, count=1, crs=f"EPSG:{epsg}",
                       width=mosaic.shape[2], height=mosaic.shape[1], transform=transform,
                       nodata=nodata, compress="deflate") as dst:
        dst.write(mosaic)
        dst.update_tags(release=release)  # the API reports this instead of a hard-coded string

    # mosaic.size provides the total cell count, v.size provides the valid cell count
    print(f"wrote {OUT}: {v.size} of {mosaic.size} cells have data ({v.size / mosaic.size:.1%}); "
          f"mm/yr min {v.min():.1f}, median {np.median(v):.1f}, max {v.max():.1f}")
          
    if np.abs(v).max() > 100:
        print("WARNING: |velocity| above 100 mm/yr is rare; check the units / scale factor of the product.")


if __name__ == "__main__":
    main()