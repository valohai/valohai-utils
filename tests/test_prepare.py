import valohai


def test_prepare():
    parameters = {
        "iambool": True,
        "mestringy": "asdf",
        "integerboi": 123,
        "floaty": 0.0001
    }
    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "myimages": [
            "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
        ]
    }

    valohai.prepare(step="test", parameters=parameters, inputs=inputs)

    assert valohai.parameters.get_parameter("iambool") == True
    assert valohai.parameters.get_parameter("mestringy") == "asdf"
    assert valohai.parameters.get_parameter("integerboi") == 123
    assert valohai.parameters.get_parameter("floaty") == 0.0001

    assert valohai.inputs.get_input_info("example").files[0].uri == \
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    assert valohai.inputs.get_input_info("myimages").files[0].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
    assert valohai.inputs.get_input_info("myimages").files[1].uri == \
        "https://upload.wikimedia.org/wikipedia/commons/0/01/Example_Wikipedia_sandbox_move_UI.png"
