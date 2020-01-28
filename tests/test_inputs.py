import json

from valohai.inputs import get_input_path
from valohai.internals.input_info import InputInfo, FileInfo


def test_get_input_paths(use_test_config_dir):
    assert get_input_path("single_image").endswith(
        "/valohai/inputs/single_image/Example.jpg"
    )
    assert get_input_path("single_image", "unused_default").endswith(
        "/valohai/inputs/single_image/Example.jpg"
    )
    assert get_input_path("nonono") == ""
    assert get_input_path("nonono", "default_path_123") == "default_path_123"


def test_inputs_serialization():
    file_data = {
        "name": "rastaboi.gz",
        "path": "/valohai/inputs/asdf/rastaboi.gz",
        "size": 6576776,
        "uri": "https://valohai-mnist.s3.amazonaws.com/rastaboi.gz",
        "checksums": {
            "md5": "ec2934etqqtadxfgataqe9c",
            "sha1": "743552wtrtrtwtrcef058b2004252c17",
            "sha256": "f7ae60f92e00ec6d435treett8c31dbd2371ec"
        }
    }

    file_result = FileInfo.serialize(FileInfo.parse(file_data))
    assert file_data == file_result

    info_data = {
        "dataset-labels": {
            "files": [
                {
                    "name": "t10k-labels-idx1-ubyte.gz",
                    "path": "/valohai/inputs/dataset-labels/t10k-labels-idx1-ubyte.gz",
                    "size": 4542,
                    "uri": "https://valohai-mnist.s3.amazonaws.com/t10k-labels-idx1-ubyte.gz",
                    "checksums": {
                        "md5": "ec29112dd5afa0611ce80d1b7f02629c",
                        "sha1": "763e7fa3757d93b0cdec073cef058b2004252c17",
                        "sha256": "f7ae60f92e00ec6debd23a6088c31dbd2371ec"
                    }
                },
                {
                    "name": "muumipeikko.zip",
                    "uri": "https://muumipeikko.com",
                }
            ]
        }
    }

    info_result = InputInfo.serialize(InputInfo.parse(info_data))
    assert info_data == info_result

