import sys
import valohai
from valohai.inputs import _get_input_info
from valohai.internals.download_type import DownloadType
from valohai.parameters import get_parameter


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

    assert get_parameter("iambool") == True
    assert get_parameter("mestringy") == "asdf"
    assert get_parameter("integerboi") == 123
    assert get_parameter("floaty") == 0.0001
    assert get_parameter("makemetrue") == True
    assert get_parameter("makemeqwer") == "qwer"
    assert get_parameter("makeme321") == 321
    assert get_parameter("makemenegative") < 0.0

    assert _get_input_info("example", download=DownloadType.NEVER).files[0].uri == \
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    assert _get_input_info("myimages", download=DownloadType.NEVER).files[0].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
    assert _get_input_info("myimages", download=DownloadType.NEVER).files[1].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
