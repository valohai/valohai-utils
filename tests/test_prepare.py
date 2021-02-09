import sys

import valohai
from valohai.internals.download_type import DownloadType
from valohai.internals.input_info import InputInfo


def test_prepare(tmpdir, monkeypatch):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)

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
        "myimages": [
            "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png",
        ],
    }

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', [
            "",
            "--makemetrue=true",
            "--makemeqwer=qwer",
            "--makeme321=321",
            "--makemenegative=-0.123",
            "--some_totally_random_parameter_to_ignore=666"
        ])
        valohai.prepare(step="test", parameters=parameters, inputs=inputs)

    assert valohai.parameters("iambool").value == True
    assert valohai.parameters("mestringy").value == "asdf"
    assert valohai.parameters("integerboi").value == 123
    assert valohai.parameters("floaty").value == 0.0001
    assert valohai.parameters("makemetrue").value == True
    assert valohai.parameters("makemeqwer").value == "qwer"
    assert valohai.parameters("makeme321").value == 321
    assert valohai.parameters("makemenegative").value < 0.0

    assert InputInfo.load("example", download=DownloadType.NEVER).files[0].uri == \
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    assert InputInfo.load("myimages", download=DownloadType.NEVER).files[0].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
    assert InputInfo.load("myimages", download=DownloadType.NEVER).files[1].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
