import numpy as np
import pytest
from rasterio.errors import RasterioIOError

import gfm_score

SCENE = {"id": "s", "properties": {"datetime": "2024-04-30T04:21:45Z"}, "assets": {"advisory_flags": {"href": "h"}}}
BAD_REPLY = "'/vsicurl/https://x/ADVFLAG_20240430T042145.tif' not recognized as being in a supported file format."


def test_a_date_in_the_file_name_is_not_a_404(monkeypatch):
    """A broken download of a file whose name holds "404" must not pass as a missing advisory layer."""
    def read_asset(item, key):
        if key == "advisory_flags":
            raise RasterioIOError(BAD_REPLY)
        return np.zeros((1, 4), "float32")
    monkeypatch.setattr(gfm_score, "read_asset", read_asset)
    with pytest.raises(RasterioIOError):
        list(gfm_score.passes([SCENE]))


@pytest.mark.parametrize("error, tries", [(BAD_REPLY, 3), ("HTTP response code: 404", 1)])
def test_read_retries_everything_but_a_404(monkeypatch, error, tries):
    calls = []

    def fail(href):
        calls.append(href)
        raise RasterioIOError(error)
    monkeypatch.setattr(gfm_score.rasterio, "open", fail)
    monkeypatch.setattr(gfm_score.time, "sleep", lambda s: None)
    with pytest.raises(RasterioIOError):
        gfm_score.read("h", attempts=3)
    assert len(calls) == tries
