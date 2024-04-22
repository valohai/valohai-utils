import os
import sys

import valohai
from valohai.internals.inputs import get_input_info


def test_prepare(tmpdir, monkeypatch):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)
    local_file = tmpdir.mkdir("sub").join("hello.txt")
    local_file.write("tiku ja taku ja joku")

    data_dir = tmpdir.mkdir("data")
    local_data = data_dir.join("data1.dat")
    local_data.write("I'm a big data")
    local_data2 = data_dir.join("data2.dat")
    local_data2.write("I'm a huge data")

    parameters = {
        "iambool": True,
        "mestringy": "asdf",
        "integerboi": 123,
        "floaty": 0.0001,
        "makemetrue": False,
        "makemefalse": True,
        "makemeqwer": "asdf",
        "makeme321": 123,
        "makemenegative": 0.0001,
        "list_bar": ["bar1", "bar2"],
    }
    url1 = "https://dist.valohai.com/valohai-utils-tests/Example.svg"
    url2 = "https://dist.valohai.com/valohai-utils-tests/sharktavern.jpg"
    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "overrideme": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "myimages": [
            url1,
            url2,
        ],
        "localdata_as_list": [str(local_data), str(local_data2)],
        "localdata_with_wildcard": os.path.join(str(data_dir), "*.dat"),
    }

    with monkeypatch.context() as m:
        args = [
            "",
            "--makemetrue=true",
            "--makemefalse=false",
            "--makemeqwer=qwer",
            "--makeme321=321",
            "--makemenegative=-0.123",
            "--some_totally_random_parameter_to_ignore=666",
            f"--overrideme={str(local_file)}",
            "--list_bar=bar1,bar2,bar3",
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
    assert valohai.parameters("makemefalse").value is False
    assert valohai.parameters("makemeqwer").value == "qwer"
    assert valohai.parameters("makeme321").value == 321
    assert valohai.parameters("makemenegative").value < 0.0
    assert valohai.parameters("list_bar").value == ["bar1", "bar2", "bar3"]

    assert (
        get_input_info("example").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    images = get_input_info("myimages").files
    assert images[0].uri == url1
    assert images[1].uri == url2
    assert not get_input_info("overrideme").files[0].uri
    assert os.path.isfile(get_input_info("overrideme").files[0].path)

    assert sum(1 for _ in valohai.inputs("localdata_as_list").paths()) == 2
    assert sum(1 for _ in valohai.inputs("localdata_with_wildcard").paths()) == 2

    for p in valohai.inputs("localdata_as_list").paths():
        assert os.path.isfile(p)

    for p in valohai.inputs("localdata_with_wildcard").paths():
        assert os.path.isfile(p)
