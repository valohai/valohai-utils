import os

import pytest

import valohai.outputs
import valohai.paths


@pytest.mark.parametrize('fragment', ("jahas.exe", "herpderp/yomomma/joo.txt"))
def test_get_output_path(outputs_path, fragment):
    path = valohai.paths.get_output_path(fragment)
    assert path == os.path.join(outputs_path, fragment)
    assert os.path.isdir(os.path.dirname(path))
