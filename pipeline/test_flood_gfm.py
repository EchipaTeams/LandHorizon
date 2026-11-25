import numpy as np
import pytest
from rasterio.errors import RasterioIOError

import flood_common
import gfm_score
from flood_gfm import before_version_change, load_checkpoint, save_checkpoint, versions

NAN = np.nan


def px(*values):
    """A 1x4 test layer."""
    return np.array([values], dtype="float32")


def scene(time, version="GFM v3.1.0", members="DLR LIST TUW"):
    on = {m: m in members.split() for m in ("DLR", "LIST", "TUW")}
    return {"id": time, "properties": {"datetime": time, "processing:version": version, "flood_members": on}}


def run(monkeypatch, layers):
    """gfm_score.passes() over fake scenes: {time: (flood, exclusion, advisory)}; advisory may be an exception."""
    def read_asset(item, key):
        layer = layers[item["id"]][("ensemble_flood_extent", "exclusion_mask", "advisory_flags").index(key)]
        if isinstance(layer, Exception):
            raise layer
        return layer
    monkeypatch.setattr(gfm_score, "read_asset", read_asset)
    monkeypatch.setattr(flood_common, "grid", lambda: (None, 4, 1))
    return list(gfm_score.passes([scene(t) for t in layers]))


MISSING = RasterioIOError("HTTP response code: 404")


@pytest.mark.parametrize("missing", [MISSING, KeyError("advisory_flags")])
def test_scene_without_advisory_layer_is_not_seen(monkeypatch, missing):
    (key, seen, flooded, used), = run(monkeypatch, {"2018-07-02T16:00:00Z": (px(1, 0, 1, 0), px(0, 0, 0, 0), missing)})
    assert key == "2018-07-02T16"
    assert not seen.any() and not flooded.any()
    assert used == []  # so gfm_versions doesn't list the pass


@pytest.mark.parametrize("order", [(0, 1), (1, 0)])
def test_missing_scene_leaves_the_rest_of_its_pass_alone(monkeypatch, order):
    """Pixel 1 is seen by both scenes, 2 and 3 only by the one with the layer, 0 only by the one without."""
    both = [("2018-07-02T16:00:00Z", (px(1, 1, NAN, NAN), px(0, 0, NAN, NAN), MISSING)),
            ("2018-07-02T16:00:25Z", (px(NAN, 0, 1, 1), px(NAN, 0, 0, 0), px(NAN, 0, 0, 2)))]
    (_, seen, flooded, used), = run(monkeypatch, dict(both[i] for i in order))
    assert [f["id"] for f in used] == ["2018-07-02T16:00:25Z"]
    assert seen.tolist() == [[False, True, True, False]]  # the last pixel is under a real flag
    assert flooded.tolist() == [[False, False, True, False]]


def test_other_advisory_errors_still_fail(monkeypatch):
    with pytest.raises(RasterioIOError):  # an outage isn't a missing layer
        run(monkeypatch, {"2018-07-02T16:00:00Z": (px(1, 0, 1, 0), px(0, 0, 0, 0), RasterioIOError("timed out"))})


def test_history_stops_at_a_major_version_change():
    v3, v4 = scene("2025-04-13T16:01:00Z"), scene("2025-04-14T04:22:00Z", "v4.0.0")
    late = scene("2025-04-16T04:00:00Z")  # a v3 scene after the change doesn't bring the history back
    assert before_version_change([late, v4, v3]) == ([v3], "2025-04-14")  # the catalogue lists newest first
    assert before_version_change([v3, scene("2025-04-12T04:00:00Z", "GFM v3.2.0")])[1] is None  # minor: no stop
    assert before_version_change([v4]) == ([v4], None)  # a history that starts in v4 is one version too


def test_version_change_within_a_day_drops_the_whole_day():
    v3, v4 = scene("2025-04-14T04:00:00Z"), scene("2025-04-14T16:00:00Z", "v4.0.0")
    assert before_version_change([v3, v4]) == ([], "2025-04-14")


@pytest.mark.parametrize("version", [None, "unknown"])
def test_unreadable_version_fails(version):
    with pytest.raises(ValueError):
        before_version_change([scene("2025-04-13T16:01:00Z", version)])


def test_versions_per_pass():
    feats = [scene("2024-05-01T16:09:00Z"), scene("2024-05-01T16:09:25Z", members="DLR TUW"),
             scene("2024-05-05T04:30:00Z")]
    assert versions(feats) == {"2024-05-01T16": ["GFM v3.1.0", "DLR TUW"],  # only what all its scenes have
                               "2024-05-05T04": ["GFM v3.1.0", "DLR LIST TUW"]}


def test_checkpoint_keeps_the_scenes_that_counted(tmp_path):
    path, zero = tmp_path / "c.npz", np.zeros((1, 4), "uint16")
    save_checkpoint(path, zero, zero, [("2018-07-02T16", np.array([1]))], {"2018-07-02T16"}, {"b", "a"})
    *_, done, used = load_checkpoint(path, (1, 4))
    assert done == {"2018-07-02T16"} and used == {"a", "b"}
    np.savez(path, **{k: v for k, v in np.load(path).items() if k != "used"})  # written before `used` existed
    assert load_checkpoint(path, (1, 4))[-1] is None
