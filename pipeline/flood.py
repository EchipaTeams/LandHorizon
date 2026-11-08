"""Flood history from Sentinel-1, computed in Earth Engine.

W1 scope: list the orbits over the AOI, build a per-orbit dry baseline,
map one event, export the result to Google Drive as a COG.

  earthengine authenticate                      # once per machine
  $env:GEE_PROJECT = "<cloud-project-id>"       # PowerShell
  uv run python pipeline/flood.py --orbits 2024-09-01 2024-10-01
  uv run python pipeline/flood.py --event 2024-09-12 2024-09-25

Output bands: n_flooded (passes that saw water), n_passes (all passes).
"""
import argparse
import os
import sys
from datetime import date

import ee

ALGORITHM_VERSION = "0.1"
# Placeholders: the dry-date test sets these before the 10-year batch.
VV_WATER_DB = -18     # flooded pixel is darker than this...
DROP_DB = -3          # ...and at least this much darker than its baseline
PERMANENT_WATER = 80  # JRC occurrence % above which a pixel is river/lake, not flood

# Provisional AOI around Galați (lon_min, lat_min, lon_max, lat_max); region locks on 15 Nov.
AOI = [27.5, 45.35, 28.25, 45.85]
CRS, SCALE = "EPSG:32635", 10  # UTM 35N, metres
# Dry window for the baseline. It must not overlap the event, or the flood darkens its own baseline.
BASELINE = (date(2023, 6, 1), date(2023, 9, 1))


def s1(aoi, start, end):
    """Sentinel-1 IW VV passes (already in dB) over the AOI."""
    return (ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(aoi)
            .filterDate(start.isoformat(), end.isoformat())
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
            .select("VV"))


def orbits(aoi, start, end):
    """Relative orbits with passes in the window. Each orbit sees the ground at its own angle."""
    return sorted(s1(aoi, start, end).aggregate_array("relativeOrbitNumber_start").distinct().getInfo())


def flood_counts(aoi, event, baseline):
    """Per pixel: how many event passes saw flood water, and how many passes there were."""
    permanent = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").unmask(0).gt(PERMANENT_WATER)
    stack = ee.ImageCollection([])
    for orbit in orbits(aoi, *event):
        same_orbit = ee.Filter.eq("relativeOrbitNumber_start", orbit)
        base_col = s1(aoi, *baseline).filter(same_orbit)
        if base_col.size().getInfo() == 0:
            print(f"orbit {orbit}: no baseline passes, skipped")
            continue
        base = base_col.median()
        flooded = s1(aoi, *event).filter(same_orbit).map(
            lambda img: img.lt(VV_WATER_DB).And(img.subtract(base).lt(DROP_DB)).And(permanent.Not()))
        stack = stack.merge(flooded)
    return ee.Image.cat(stack.sum().rename("n_flooded"), stack.count().rename("n_passes")).toUint16()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--orbits", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="list orbits with passes in this window")
    mode.add_argument("--event", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="map floods in this window and export a COG to Drive")
    p.add_argument("--baseline", nargs=2, type=date.fromisoformat, metavar=("START", "END"), default=BASELINE)
    a = p.parse_args()

    if a.event:  # check inputs before spending time on the Earth Engine login
        start, end = a.event
        b_start, b_end = a.baseline
        if b_start < end and start < b_end:
            sys.exit("Baseline overlaps the event window; pick a dry period outside it.")

    project = os.environ.get("GEE_PROJECT") or sys.exit("Set GEE_PROJECT to your Earth Engine Cloud project id.")
    ee.Initialize(project=project)
    aoi = ee.Geometry.Rectangle(AOI)

    if a.orbits:
        print("orbits:", orbits(aoi, *a.orbits))
        return

    name = f"flood_{start}_{end}_v{ALGORITHM_VERSION.replace('.', '-')}"
    task = ee.batch.Export.image.toDrive(
        image=flood_counts(aoi, a.event, a.baseline).clip(aoi),
        description=name, folder="landhorizon", fileNamePrefix=name,
        region=aoi, scale=SCALE, crs=CRS, maxPixels=1e10,
        formatOptions={"cloudOptimized": True},
    )
    task.start()
    print(f"started {name} (task {task.id}); watch it at https://code.earthengine.google.com/tasks")


if __name__ == "__main__":
    main()
