import json

from valohai.utils import get_parameters_config_json, get_inputs_config_json


def test_inputs_prepare():
    source_inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "myimages": [
            "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
        ]
    }

    result = json.loads(get_inputs_config_json(source_inputs))

    assert {'uri': 'https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz'} in result['example']['files']
    assert {'uri': 'https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg'} in result['myimages']['files']
    assert {'uri': 'https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png'} \
           in result['myimages']['files']


def test_parameters_prepare():
    source_parameters = {
      "iambool": True,
      "mestringy": "muumipeikko on irstas gigolo",
      "integerpderp": 524252,
      "floater": 0.0023,
    }

    result = json.loads(get_parameters_config_json(source_parameters))

    assert result["iambool"] == True
    assert result["mestringy"] == "muumipeikko on irstas gigolo"
    assert result["integerpderp"] == 524252
    assert result["floater"] == 0.0023
