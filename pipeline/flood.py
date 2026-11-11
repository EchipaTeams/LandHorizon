"""Flood history from Sentinel-1, computed in Earth Engine.

W1 scope: list the orbits over the AOI, build a per-orbit dry baseline,
map one event, export the result to Google Drive as a COG.

  earthengine authenticate                      # once per machine
  $env:GEE_PROJECT = "<cloud-project-id>"       # PowerShell
  uv run python pipeline/flood.py --orbits 2024-09-01 2024-10-01
  uv run python pipeline/flood.py --event 2024-09-12 2024-09-25
  uv run python pipeline/flood.py --evaluate 2023-09-12 2023-09-25            # dry-date test
  uv run python pipeline/flood.py --evaluate 2024-09-12 2024-09-25 \\
      --reference data/raw/reference/EMSR758_AOI03_DEL_PRODUCT_v1.zip        # vs Copernicus EMS

Output bands: n_flooded (passes that saw water), n_passes (all passes).
--evaluate prints scores instead of exporting, and accepts threshold overrides
for tuning. Exports always use the constants below, so the version label stays true.
"""
import argparse
import json
import os
import sys
import zipfile
from datetime import date

import ee

ALGORITHM_VERSION = "0.2"
# Tuned 10 Nov 2026 against the dry-date test; runs and results in docs/flood-validation.md.
VV_WATER_DB = -18     # flooded pixel is darker than this...
DROP_DB = -4          # ...and at least this much darker than its baseline
PERMANENT_WATER = 80  # JRC occurrence % above which a pixel is river/lake, not flood
SPECKLE_M = 30        # focal median radius applied to each pass before thresholding; 0 = off
HAND_MAX_M = 10       # if set, only pixels at most this high above drainage (MERIT Hydro) can flood
VH_WATER_DB = -24     # if set, a flooded pixel must also be darker than this in VH (cross-polarised)

# Provisional AOI around Galați (lon_min, lat_min, lon_max, lat_max); region locks on 15 Nov.
AOI = [27.5, 45.35, 28.25, 45.85]
CRS, SCALE = "EPSG:32635", 10  # UTM 35N, metres
# Dry window for the baseline. It must not overlap the event, or the flood darkens its own baseline.
BASELINE = (date(2023, 6, 1), date(2023, 9, 1))


def s1(aoi, start, end, bands=("VV",)):
    """Sentinel-1 IW passes (already in dB) over the AOI that carry all the given polarisations."""
    col = (ee.ImageCollection("COPERNICUS/S1_GRD")
           .filterBounds(aoi)
           .filterDate(start.isoformat(), end.isoformat())
           .filter(ee.Filter.eq("instrumentMode", "IW")))
    for band in bands:
        col = col.filter(ee.Filter.listContains("transmitterReceiverPolarisation", band))
    return col.select(list(bands))


def orbits(aoi, start, end):
    """Relative orbits with passes in the window. Each orbit sees the ground at its own angle."""
    return sorted(s1(aoi, start, end).aggregate_array("relativeOrbitNumber_start").distinct().getInfo())


def permanent_water():
    return ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").unmask(0).gt(PERMANENT_WATER)


def flood_counts(aoi, event, baseline, water_db=VV_WATER_DB, drop_db=DROP_DB,
                 speckle_m=SPECKLE_M, hand_max_m=HAND_MAX_M, vh_db=VH_WATER_DB):
    """Per pixel: how many event passes saw flood water, and how many passes there were."""
    can_flood = permanent_water().Not()
    if hand_max_m is not None:  # unmask: MERIT has no HAND over its own water bodies, which are low anyway
        can_flood = can_flood.And(ee.Image("MERIT/Hydro/v1_0_1").select("hnd").unmask(0).lte(hand_max_m))

    bands = ("VV",) if vh_db is None else ("VV", "VH")

    def is_flooded(img, base):
        if speckle_m:
            img = img.focalMedian(speckle_m, "circle", "meters").rename(list(bands))
        vv = img.select("VV")
        water = vv.lt(water_db).And(vv.subtract(base.select("VV")).lt(drop_db)).And(can_flood)
        if vh_db is not None:
            water = water.And(img.select("VH").lt(vh_db))
        return water

    stack = ee.ImageCollection([])
    for orbit in orbits(aoi, *event):
        same_orbit = ee.Filter.eq("relativeOrbitNumber_start", orbit)
        base_col = s1(aoi, *baseline, bands).filter(same_orbit)
        if base_col.size().getInfo() == 0:
            print(f"orbit {orbit}: no baseline passes, skipped")
            continue
        base = base_col.median()
        stack = stack.merge(s1(aoi, *event, bands).filter(same_orbit).map(lambda img: is_flooded(img, base)))
    return ee.Image.cat(stack.sum().rename("n_flooded"), stack.count().rename("n_passes")).toUint16()


def ems_layer(path, suffix):
    """One GeoJSON layer from a Copernicus EMS delineation zip, e.g. 'observedEventA'."""
    with zipfile.ZipFile(path) as zf:
        name = next(n for n in zf.namelist() if n.endswith(f"{suffix}_v1.json"))
        return ee.FeatureCollection(json.loads(zf.read(name)))


def evaluate(aoi, counts, reference=None):
    """Print the share of land flagged flooded; with an EMS zip, also precision and recall inside its AOI."""
    n_flooded, n_passes = counts.select("n_flooded"), counts.select("n_passes")
    flagged = ee.Image.cat([n_flooded.gte(k).rename(f"ge{k}") for k in (1, 2, 3)])
    stats = dict(scale=SCALE, crs=CRS, maxPixels=1e10, tileScale=4)

    land = n_passes.gt(0).And(permanent_water().Not())
    share = flagged.updateMask(land).reduceRegion(ee.Reducer.mean(), aoi, **stats).getInfo()
    print("land flagged flooded:  " + "  ".join(f">={k} pass: {share[f'ge{k}']:6.2%}" for k in (1, 2, 3)))
    if not reference:
        return

    ref = ee.Image(0).paint(ems_layer(reference, "observedEventA"), 1).rename("ref")
    valid = n_passes.gt(0)
    bands = [ref] + [flagged.select(f"ge{k}").rename(f"pred{k}") for k in (1, 2, 3)] + \
            [flagged.select(f"ge{k}").And(ref).rename(f"tp{k}") for k in (1, 2, 3)]
    s = ee.Image.cat(bands).updateMask(valid).reduceRegion(
        ee.Reducer.sum().unweighted(), ems_layer(reference, "areaOfInterestA").geometry(), **stats).getInfo()
    print(f"reference {os.path.basename(reference)}: {s['ref'] / 100:.0f} ha flooded")
    for k in (1, 2, 3):
        prec = s[f"tp{k}"] / s[f"pred{k}"] if s[f"pred{k}"] else float("nan")
        print(f"  flooded in >= {k} pass(es): predicted {s[f'pred{k}'] / 100:8.0f} ha  "
              f"precision {prec:6.1%}  recall {s[f'tp{k}'] / s['ref']:6.1%}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--orbits", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="list orbits with passes in this window")
    mode.add_argument("--event", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="map floods in this window and export a COG to Drive")
    mode.add_argument("--evaluate", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="map floods in this window and print scores (no export)")
    p.add_argument("--baseline", nargs=2, type=date.fromisoformat, metavar=("START", "END"), default=BASELINE)
    p.add_argument("--reference", help="Copernicus EMS delineation zip to score against (--evaluate only)")
    tune = p.add_argument_group("tuning overrides (--evaluate only; defaults are the constants)")
    tune.add_argument("--water-db", type=float, default=VV_WATER_DB)
    tune.add_argument("--drop-db", type=float, default=DROP_DB)
    tune.add_argument("--speckle-m", type=float, default=SPECKLE_M)
    tune.add_argument("--hand-max-m", type=float, default=HAND_MAX_M)
    tune.add_argument("--vh-db", type=float, default=VH_WATER_DB)
    a = p.parse_args()

    overrides = dict(water_db=a.water_db, drop_db=a.drop_db, speckle_m=a.speckle_m,
                     hand_max_m=a.hand_max_m, vh_db=a.vh_db)
    defaults = dict(water_db=VV_WATER_DB, drop_db=DROP_DB, speckle_m=SPECKLE_M,
                    hand_max_m=HAND_MAX_M, vh_db=VH_WATER_DB)
    if not a.evaluate and (overrides != defaults or a.reference):
        p.error("--reference and the tuning overrides only work with --evaluate")
    window = a.event or a.evaluate
    if window:  # check inputs before spending time on the Earth Engine login
        start, end = window
        b_start, b_end = a.baseline
        if b_start < end and start < b_end:
            sys.exit("Baseline overlaps the event window; pick a dry period outside it.")
        if a.reference and not os.path.exists(a.reference):
            sys.exit(f"No such reference file: {a.reference}")

    project = os.environ.get("GEE_PROJECT") or sys.exit("Set GEE_PROJECT to your Earth Engine Cloud project id.")
    ee.Initialize(project=project)
    aoi = ee.Geometry.Rectangle(AOI)

    if a.orbits:
        print("orbits:", orbits(aoi, *a.orbits))
        return

    if a.evaluate:
        print(f"window {start}..{end}, baseline {b_start}..{b_end}, " +
              ", ".join(f"{k}={v}" for k, v in overrides.items()))
        evaluate(aoi, flood_counts(aoi, a.evaluate, a.baseline, **overrides), a.reference)
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
