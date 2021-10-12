import json
import sys

import valohai
from valohai.internals.download_type import DownloadType
from valohai.internals.input_info import get_input_info

# Inputs and parameters can come from (in the order of priority):
#
# 1. Command-line
# 2. parameters.json and inputs.json configs
# 3. Call to valohai.prepare()
#
# Here we test that the priority order is honored


def test_parsing_priorities(tmpdir, monkeypatch):
    local_file = tmpdir.mkdir("sub").join("hello.txt")
    local_file.write("tiku ja taku ja joku")

    parameters = {
        "floaty": 0.0001,
    }
    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
    }

    with monkeypatch.context() as m:
        # 1. Test that default_parameters and default_inputs work from .prepare()
        valohai.prepare(
            step="test", default_parameters=parameters, default_inputs=inputs
        )
        assert (
            get_input_info("example", download=DownloadType.NEVER).files[0].uri
            == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
        )
        assert valohai.parameters("floaty").value == 0.0001

        # 2. Test that parameters.json and inputs.json take priority over defaults from .prepare()
        config_dir = tmpdir.mkdir("configs")
        inputs_json = config_dir.join("inputs.json")
        parameters_json = config_dir.join("parameters.json")

        inputs_json.write(
            json.dumps(
                {
                    "example": {
                        "files": [
                            {
                                "name": "example.svg",
                                "uri": "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg",
                                "path": None,
                                "size": 0,
                                "checksums": [],
                            }
                        ]
                    }
                }
            )
        )
        parameters_json.write(json.dumps({"floaty": 0.5}))
        m.setenv("VH_CONFIG_DIR", config_dir)
        valohai.prepare(
            step="test", default_parameters=parameters, default_inputs=inputs
        )
        assert (
            get_input_info("example", download=DownloadType.NEVER).files[0].uri
            == "https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg"
        )
        assert valohai.parameters("floaty").value == 0.5

        # 3. Test that command-line parameters take priority over parameters.json and inputs.json
        args = [
            "",
            "--floaty=0.999",
            "--example=https://www.parsedfromcommandline.com/yeah.txt",
        ]
        m.setattr(
            sys,
            "argv",
            args,
        )
        valohai.prepare(
            step="test", default_parameters=parameters, default_inputs=inputs
        )
        assert (
            get_input_info("example", download=DownloadType.NEVER).files[0].uri
            == "https://www.parsedfromcommandline.com/yeah.txt"
        )
        assert valohai.parameters("floaty").value == 0.999
