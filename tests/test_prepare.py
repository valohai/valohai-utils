import os
import sys

import valohai
from valohai.internals.inputs import get_input_info


def test_prepare(tmpdir, monkeypatch):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)
    local_file = tmpdir.mkdir("sub").join("hello.txt")
    local_file.write("tiku ja taku ja joku")

    parameters = {
        "iambool": True,
        "mestringy": "asdf",
        "integerboi": 123,
        "floaty": 0.0001,
        "makemetrue": False,
        "makemeqwer": "asdf",
        "makeme321": 123,
        "makemenegative": 0.0001,
    }
    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "overrideme": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "myimages": [
            "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png",
        ],
    }

    with monkeypatch.context() as m:
        args = [
            "",
            "--makemetrue=true",
            "--makemeqwer=qwer",
            "--makeme321=321",
            "--makemenegative=-0.123",
            "--some_totally_random_parameter_to_ignore=666",
            f"--overrideme={str(local_file)}",
        ]
        m.setattr(
            sys,
            "argv",
            args,
        )
        valohai.prepare(
            step="test", default_parameters=parameters, default_inputs=inputs
        )

    assert valohai.parameters("iambool").value is True
    assert valohai.parameters("mestringy").value == "asdf"
    assert valohai.parameters("integerboi").value == 123
    assert valohai.parameters("floaty").value == 0.0001
    assert valohai.parameters("makemetrue").value is True
    assert valohai.parameters("makemeqwer").value == "qwer"
    assert valohai.parameters("makeme321").value == 321
    assert valohai.parameters("makemenegative").value < 0.0

    assert (
        get_input_info("example").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    assert (
        get_input_info("myimages").files[0].uri
        == "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
    )
    assert (
        get_input_info("myimages").files[1].uri
        == "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
    )
    assert not get_input_info("overrideme").files[0].uri
    assert os.path.isfile(get_input_info("overrideme").files[0].path)
