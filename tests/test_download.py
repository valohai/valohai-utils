import os
import sys

import valohai
from valohai.internals.input_info import InputInfo, load_input_info


def test_download(tmpdir, monkeypatch, requests_mock):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)

    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    requests_mock.get("https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg")
    requests_mock.get(
        "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
    )

    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "myimages": [
            "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png",
        ],
    }

    monkeypatch.setattr(sys, "argv", ["myscript.py"])
    valohai.prepare(step="test", default_inputs=inputs)

    # These calls will trigger downloads
    assert (
        load_input_info("example").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    assert (
        load_input_info("myimages").files[0].uri
        == "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
    )
    assert (
        load_input_info("myimages").files[1].uri
        == "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
    )

    assert requests_mock.call_count == 3

    assert os.path.isfile(
        os.path.join(inputs_dir, "example", "t10k-images-idx3-ubyte.gz")
    )
    assert os.path.isfile(os.path.join(inputs_dir, "myimages", "Example.svg"))
    assert os.path.isfile(
        os.path.join(inputs_dir, "myimages", "Example_Wikipedia_sandbox_move_UI.png")
    )

    # Second time around, the file should be cached and not trigger any more downloads
    load_input_info("myimages")
    assert requests_mock.call_count == 3
