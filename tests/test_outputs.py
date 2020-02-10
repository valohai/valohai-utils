import os

import pytest

import valohai.outputs
import valohai.paths


@pytest.mark.parametrize('fragment', ("jahas.exe", "herpderp/yomomma/joo.txt"))
def test_get_output_path(outputs_path, fragment):
    path = valohai.paths.get_output_path(fragment)
    assert path == os.path.join(outputs_path, fragment)
    assert os.path.isdir(os.path.dirname(path))


def test_live_upload(outputs_path):
    path = valohai.paths.get_output_path("hello.zip")
    with open(path, "w") as fp:
        fp.write('hello')
    valohai.outputs.live_upload(path)

    with pytest.raises(IOError):
        # Test the file is set read-only
        open(path, "w")