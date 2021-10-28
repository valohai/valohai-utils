import os
import sys

import valohai
from valohai.internals.inputs import get_input_info, get_input_vfs


def test_download(tmpdir, monkeypatch, requests_mock):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)

    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz"
    )
    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz"
    )

    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "mnist": [
            "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz",
            "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz",
        ],
    }

    monkeypatch.setattr(sys, "argv", ["myscript.py"])
    valohai.prepare(step="test", default_inputs=inputs)

    # These calls will trigger downloads
    get_input_vfs("example")
    get_input_vfs("mnist")

    assert (
        get_input_info("example").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    assert (
        get_input_info("mnist").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz"
    )
    assert (
        get_input_info("mnist").files[1].uri
        == "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz"
    )
    assert requests_mock.call_count == 3

    assert os.path.isfile(
        os.path.join(inputs_dir, "example", "t10k-images-idx3-ubyte.gz")
    )
    assert os.path.isfile(
        os.path.join(inputs_dir, "mnist", "train-images-idx3-ubyte.gz")
    )
    assert os.path.isfile(
        os.path.join(inputs_dir, "mnist", "train-labels-idx1-ubyte.gz")
    )

    # Second time around, the file should be cached and not trigger any more downloads
    get_input_vfs("mnist")
    get_input_vfs("example")

    assert requests_mock.call_count == 3
