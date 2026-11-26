"""Old-format Copernicus EMS vector zip (shapefiles, before ~2022) -> the zip layout flood_common.ems() reads.

EMSR293 (Botoșani, July 2018) is only published in the old format, from
https://mapping.emergency.copernicus.eu/activations/EMSR293 (the *_DELINEATION_*_vector.zip files).

  uv run --with pyshp python checks/ems_reference/convert_old_format.py \\
      EMSR293_01BOTOSANI_01DELINEATION_MAP_v1_vector.zip EMSR293_AOI01_DEL_PRODUCT \\
      data/raw/reference/EMSR293_AOI01_DEL_PRODUCT_v1.zip
  (and _01DELINEATION_MONIT01_v1_vector.zip -> EMSR293_AOI01_DEL_MONIT01 / ..._MONIT01_v1.zip)

Every feature of observed_event_a and area_of_interest_a is kept, as lon/lat GeoJSON. Check used in F2
(docs/flood-validation.md): 313.6 and 373.3 ha of flood on the grid, against the 314 and 373 ha EMS reports.
"""
import io
import json
import sys
import zipfile

import shapefile  # pyshp, only for this one-off: uv run --with pyshp

old, prefix, out = sys.argv[1:]
with zipfile.ZipFile(old) as zf:
    names = zf.namelist()

    def layer(suffix):
        base = next(n[:-4] for n in names if n.endswith(f"_{suffix}.shp"))
        prj = zf.read(base + ".prj").decode()
        assert "WGS_1984" in prj and "PROJCS" not in prj, prj  # lon/lat WGS84, as ems() assumes
        r = shapefile.Reader(shp=io.BytesIO(zf.read(base + ".shp")), shx=io.BytesIO(zf.read(base + ".shx")),
                             dbf=io.BytesIO(zf.read(base + ".dbf")))
        feats = [{"type": "Feature", "properties": dict(sr.record.as_dict()), "geometry": sr.shape.__geo_interface__}
                 for sr in r.shapeRecords()]
        print(f"{base}: {len(feats)} features, types {sorted({f['geometry']['type'] for f in feats})}")
        return {"type": "FeatureCollection", "features": feats}

    event, aoi = layer("observed_event_a"), layer("area_of_interest_a")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr(f"{prefix}_observedEventA_v1.json", json.dumps(event, default=str))
    zf.writestr(f"{prefix}_areaOfInterestA_v1.json", json.dumps(aoi, default=str))
print("wrote", out)
