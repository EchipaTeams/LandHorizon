"""Flood history from Sentinel-1, computed locally: no Earth Engine, no quota (prototype).

Downloads GRD scenes from the Copernicus Data Space Ecosystem (free account), runs ESA SNAP
on each (pipeline/s1_preprocess.xml: the same chain as Earth Engine's COPERNICUS/S1_GRD), keeps
only the AOI as a small per-pass cache, then applies flood_earthengine.py's method and thresholds in numpy.

  set -a; source .env; set +a      # CDSE_USER / CDSE_PASSWORD (dataspace.copernicus.eu)
  uv run python pipeline/flood_local.py --event 2024-09-12 2024-09-25
  uv run python pipeline/flood_local.py --evaluate 2023-09-12 2023-09-25                  # dry-date test
  uv run python pipeline/flood_local.py --evaluate 2024-09-12 2024-09-25 \\
      --reference data/raw/reference/EMSR758_AOI03_DEL_PRODUCT_v1.zip                     # vs Copernicus EMS

Output: data/processed/flood_<start>_<end>_v<version>-local.tif, bands n_flooded, n_passes,
on the same grid as flood_earthengine.py's export. Passes already in data/raw/s1/aoi/ are never re-downloaded,
so reruns and tuning cost nothing. SNAP: set SNAP_GPT if gpt isn't at ~/esa-snap/bin/gpt.
"""
import argparse
import http.client
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import median_filter

from flood_common import CRS, OUT, ROOT, SCALE, aoi_wkt, grid, masks, report, to_grid, write_counts
from flood_earthengine import (ALGORITHM_VERSION, BASELINE, DROP_DB, HAND_MAX_M, PERMANENT_WATER, SPECKLE_M,
                               VH_WATER_DB, VV_WATER_DB)

RAW = ROOT / "data" / "raw" / "s1"   # downloaded zips (deleted after SNAP unless --keep-raw)
CACHE = RAW / "aoi"                  # one small GeoTIFF per scene: VV, VH in dB on the AOI grid
GRAPH = Path(__file__).with_name("s1_preprocess.xml")
GPT = os.environ.get("SNAP_GPT", str(Path.home() / "esa-snap" / "bin" / "gpt"))

CATALOGUE = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
DOWNLOAD = "https://zipper.dataspace.copernicus.eu/odata/v1/Products({})/$value"


# --- Copernicus Data Space: find and download scenes ------------------------------------------

def search(start, end):
    """IW GRD scenes over the AOI in [start, end), as dicts with id, name, date, orbit."""
    flt = (f"Collection/Name eq 'SENTINEL-1' and contains(Name,'IW_GRDH') "
           f"and OData.CSC.Intersects(area=geography'SRID=4326;{aoi_wkt()}') "
           f"and ContentDate/Start ge {start.isoformat()}T00:00:00.000Z "
           f"and ContentDate/Start lt {end.isoformat()}T00:00:00.000Z")
    url = CATALOGUE + "?" + urllib.parse.urlencode(
        {"$filter": flt, "$expand": "Attributes", "$top": 100, "$orderby": "ContentDate/Start"})
    scenes = []
    while url:
        page = json.load(urllib.request.urlopen(url, timeout=120))
        for p in page["value"]:
            if p["Name"].endswith("_COG.SAFE"):  # same data, other packaging; SNAP reads the standard SAFE
                continue
            attrs = {a["Name"]: a["Value"] for a in p["Attributes"]}
            scenes.append({"id": p["Id"], "name": p["Name"].removesuffix(".SAFE"),
                           "date": p["ContentDate"]["Start"][:10], "orbit": int(attrs["relativeOrbitNumber"])})
        url = page.get("@odata.nextLink")
    return scenes


def token():
    user, password = os.environ.get("CDSE_USER"), os.environ.get("CDSE_PASSWORD")
    if not (user and password):
        sys.exit("Set CDSE_USER and CDSE_PASSWORD (free account at dataspace.copernicus.eu), e.g. in .env.")
    data = urllib.parse.urlencode({"grant_type": "password", "username": user, "password": password,
                                   "client_id": "cdse-public"}).encode()
    return json.load(urllib.request.urlopen(TOKEN_URL, data=data, timeout=60))["access_token"]


def download(scene, attempts=6):
    """The scene's zip in data/raw/s1/.

    Long downloads get cut off now and then ("connection reset"), so retry, resuming from the bytes
    already in the .part file. The zip only gets its real name once its size matches what the server
    announced, so a truncated file can't pass as complete.
    """
    path = RAW / f"{scene['name']}.zip"
    if path.exists():
        return path
    RAW.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(".part")
    for attempt in range(1, attempts + 1):
        have = part.stat().st_size if part.exists() else 0
        headers = {"Authorization": f"Bearer {token()}"}  # fresh token each try: they expire after 10 minutes
        if have:
            headers["Range"] = f"bytes={have}-"
        try:
            with urllib.request.urlopen(urllib.request.Request(DOWNLOAD.format(scene["id"]), headers=headers),
                                        timeout=300) as r:
                if r.status != 206:  # server ignored the range: start over
                    have = 0
                expected = have + int(r.headers["Content-Length"])
                with open(part, "ab" if have else "wb") as f:
                    while chunk := r.read(1 << 22):
                        f.write(chunk)
            if part.stat().st_size == expected:
                part.replace(path)
                return path
            print(f"  {scene['name']}: got {part.stat().st_size} of {expected} bytes, retrying", flush=True)
        except (OSError, http.client.HTTPException) as e:  # URLError, resets and timeouts are OSErrors
            if getattr(e, "code", None) == 416:  # "range not satisfiable": the .part is unusable, start over
                part.unlink()
            if attempt == attempts:
                raise
            print(f"  {scene['name']}: download interrupted ({e}), retry {attempt}/{attempts - 1}", flush=True)
        time.sleep(15 * attempt)
    raise RuntimeError(f"{scene['name']}: download kept coming up short after {attempts} attempts")


# --- SNAP: one scene -> VV, VH in dB on the AOI grid -------------------------------------------

def prefetched(scenes, workers=2, ahead=3):
    """(scene, zip path) in order, while up to `workers` downloads run in the background.

    At most `ahead` zips are downloading or waiting at once (~1.7 GB each), so disk use stays bounded.
    Daemon threads: Ctrl+C stops at once instead of waiting for downloads in flight.
    """
    jobs, room = queue.Queue(), threading.Semaphore(ahead)
    results = [queue.Queue(maxsize=1) for _ in scenes]
    for i in range(len(scenes)):
        jobs.put(i)

    def work():
        while True:
            room.acquire()  # before taking a job, so downloads start in order and can't deadlock
            try:
                i = jobs.get_nowait()
            except queue.Empty:
                room.release()
                return
            try:
                results[i].put((download(scenes[i]), None))
            except Exception as e:
                results[i].put((None, e))

    for _ in range(workers):
        threading.Thread(target=work, daemon=True).start()
    for i, scene in enumerate(scenes):
        path, error = results[i].get()
        room.release()
        if error:
            raise error
        yield scene, path


def cache_path(scene):
    return CACHE / f"{scene['date']}_{scene['orbit']:03d}_{scene['name'][-4:]}.tif"


def preprocess(scene, zip_path, keep_raw=False):
    """Run SNAP on a downloaded scene and cache its AOI crop (bands VV, VH in dB on the AOI grid)."""
    cached = cache_path(scene)
    snap_out = RAW / f"{scene['name']}_snap.tif"
    subprocess.run([GPT, str(GRAPH), f"-Pinput={zip_path}", f"-Poutput={snap_out}", f"-Paoi={aoi_wkt()}",
                    "-q", str(os.cpu_count())], check=True, stdout=subprocess.DEVNULL)

    with rasterio.open(snap_out) as src:
        names = band_names(src)
        bands = {}
        for pol in ("VV", "VH"):
            a = to_grid(src, names.index(f"Sigma0_{pol}_db") + 1)
            a[(a == 0) | ~np.isfinite(a)] = np.nan  # SNAP writes 0 for "no data", even after the dB step
            bands[pol] = a
    CACHE.mkdir(parents=True, exist_ok=True)
    transform, width, height = grid()
    part = cached.with_suffix(".part")  # renamed only when complete: a power cut never leaves a fake "done" scene
    with rasterio.open(part, "w", driver="GTiff", dtype="float32", count=2, crs=CRS, transform=transform,
                       width=width, height=height, nodata=np.nan, compress="deflate", tiled=True) as dst:
        dst.write(np.stack([bands["VV"], bands["VH"]]))
        dst.descriptions = ("VV", "VH")
    part.replace(cached)
    snap_out.unlink()
    if not keep_raw:
        zip_path.unlink()
    return cached


def band_names(src):
    """SNAP's band names (e.g. Sigma0_VV_db), in band order.

    GeoTIFF-BigTIFF keeps them in a DIMAP XML header near the start of the file, in a private
    TIFF tag GDAL doesn't expose, so read the raw bytes: each <BAND_INDEX> is followed by its <BAND_NAME>.
    """
    with open(src.name, "rb") as f:
        header = f.read(1 << 20).decode("latin-1")
    pairs = re.findall(r"<BAND_INDEX>(\d+)</BAND_INDEX>(?:(?!<BAND_INDEX>).)*?<BAND_NAME>([^<]+)</BAND_NAME>",
                       header, re.DOTALL)
    names = [name for _, name in sorted((int(i), name) for i, name in pairs)]
    if len(names) != src.count or not {"Sigma0_VV_db", "Sigma0_VH_db"} <= set(names):
        sys.exit(f"Can't tell the VV/VH band order in {src.name} (found {names}); check the SNAP output.")
    return names


def fetch(scenes, keep_raw=False):
    """Make sure every scene is in the cache: download (in the background) and SNAP the missing ones."""
    todo = [s for s in scenes if not cache_path(s).exists()]
    print(f"{len(scenes)} scenes, {len(scenes) - len(todo)} already cached", flush=True)
    for n, (s, zip_path) in enumerate(prefetched(todo), 1):
        print(f"  [{n}/{len(todo)}] SNAP {s['name']} ...", flush=True)
        preprocess(s, zip_path, keep_raw)


def passes(scenes):
    """{orbit: [(date, VV, VH), ...]} from cached scenes. Frames of the same pass are merged."""
    frames = defaultdict(list)
    for s in scenes:
        frames[(s["orbit"], s["date"])].append(cache_path(s))
    out = defaultdict(list)
    for (orbit, day), paths in sorted(frames.items()):
        vv = vh = None
        for p in paths:
            with rasterio.open(p) as src:
                a, b = src.read(1), src.read(2)
            vv = a if vv is None else np.where(np.isnan(vv), a, vv)
            vh = b if vh is None else np.where(np.isnan(vh), b, vh)
        out[orbit].append((day, vv, vh))
    return out


# --- The method (pure numpy, tested in test_flood_local.py) ------------------------------------

def smooth(a, radius_m):
    """Focal median over a disk, like Earth Engine's focalMedian. No-data pixels stay no-data."""
    r = round(radius_m / SCALE)
    if r < 1:
        return a
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    nan = np.isnan(a)
    # ponytail: no-data is filled with 0 dB (bright, never water) for the filter; EE ignores it instead.
    out = median_filter(np.where(nan, 0, a), footprint=x * x + y * y <= r * r)
    out[nan] = np.nan
    return out


def flood_counts(event, baseline, can_flood, water_db=VV_WATER_DB, drop_db=DROP_DB,
                 speckle_m=SPECKLE_M, vh_db=VH_WATER_DB):
    """Per pixel: how many event passes saw flood water, and how many passes there were.

    event: {orbit: [(date, VV, VH), ...]} in dB; baseline: {orbit: VV median in dB}; can_flood: bool array.
    """
    shape = can_flood.shape
    n_flooded, n_passes = np.zeros(shape, "uint16"), np.zeros(shape, "uint16")
    for orbit, items in event.items():
        if orbit not in baseline:
            print(f"orbit {orbit}: no baseline passes, skipped")
            continue
        base = baseline[orbit]
        for _, vv, vh in items:
            vv = smooth(vv, speckle_m)
            valid = np.isfinite(vv) & np.isfinite(base)
            water = (vv < water_db) & (vv - base < drop_db) & can_flood
            if vh_db is not None:
                vh = smooth(vh, speckle_m)
                valid &= np.isfinite(vh)
                water &= vh < vh_db
            n_passes += valid
            n_flooded += valid & water
    return n_flooded, n_passes


def run(window, baseline_window, keep_raw, **params):
    hand_max_m, permanent_water = params.pop("hand_max_m"), params.pop("permanent_water")
    event_scenes = search(*window)
    orbits = {s["orbit"] for s in event_scenes}
    base_scenes = [s for s in search(*baseline_window) if s["orbit"] in orbits]  # other orbits aren't needed
    print(f"event {window[0]}..{window[1]}: {len(event_scenes)} scenes; "
          f"baseline {baseline_window[0]}..{baseline_window[1]}: {len(base_scenes)} scenes", flush=True)
    fetch(event_scenes + base_scenes, keep_raw)  # one queue, so downloads overlap SNAP across both windows

    event = passes(event_scenes)
    baseline = {orbit: np.nanmedian(np.stack([vv for _, vv, _ in items]), axis=0)
                for orbit, items in passes(base_scenes).items()}
    permanent, can_flood = masks(hand_max_m, permanent_water)
    return (*flood_counts(event, baseline, can_flood, **params), permanent)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--event", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="map floods in this window and write a COG to data/processed/")
    mode.add_argument("--evaluate", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
                      help="map floods in this window and print scores (no file written)")
    p.add_argument("--baseline", nargs=2, type=date.fromisoformat, metavar=("START", "END"), default=BASELINE)
    p.add_argument("--reference", help="Copernicus EMS delineation zip to score against (--evaluate only)")
    p.add_argument("--keep-raw", action="store_true", help="keep downloaded zips (about 1.7 GB each)")
    tune = p.add_argument_group("tuning overrides (--evaluate only; defaults are flood_earthengine.py's constants)")
    tune.add_argument("--water-db", type=float, default=VV_WATER_DB)
    tune.add_argument("--drop-db", type=float, default=DROP_DB)
    tune.add_argument("--speckle-m", type=float, default=SPECKLE_M)
    tune.add_argument("--hand-max-m", type=float, default=HAND_MAX_M)
    tune.add_argument("--vh-db", type=float, default=VH_WATER_DB)
    tune.add_argument("--permanent-water", type=float, default=PERMANENT_WATER,
                      help="JRC occurrence %% above which a pixel is water, not land (default %(default)s)")
    a = p.parse_args()

    params = dict(water_db=a.water_db, drop_db=a.drop_db, speckle_m=a.speckle_m,
                  hand_max_m=a.hand_max_m, vh_db=a.vh_db, permanent_water=a.permanent_water)
    defaults = dict(water_db=VV_WATER_DB, drop_db=DROP_DB, speckle_m=SPECKLE_M,
                    hand_max_m=HAND_MAX_M, vh_db=VH_WATER_DB, permanent_water=PERMANENT_WATER)
    if a.event and (params != defaults or a.reference):
        p.error("--reference and the tuning overrides only work with --evaluate")
    start, end = a.event or a.evaluate
    b_start, b_end = a.baseline
    if b_start < end and start < b_end:
        sys.exit("Baseline overlaps the event window; pick a dry period outside it.")
    if a.reference and not os.path.exists(a.reference):
        sys.exit(f"No such reference file: {a.reference}")

    print(f"window {start}..{end}, baseline {b_start}..{b_end}, " + ", ".join(f"{k}={v}" for k, v in params.items()))
    n_flooded, n_passes, permanent = run((start, end), a.baseline, a.keep_raw, **params)

    if a.evaluate:
        report(n_flooded, n_passes, permanent, a.reference)
        return
    write_counts(OUT / f"flood_{start}_{end}_v{ALGORITHM_VERSION.replace('.', '-')}-local.tif", n_flooded, n_passes)


if __name__ == "__main__":
    main()
