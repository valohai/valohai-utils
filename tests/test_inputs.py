import os

import valohai


def test_get_input_paths(use_test_config_dir):
    assert valohai.inputs("single_image").path().endswith("single_image/Example.jpg")
    assert os.path.exists(valohai.inputs("single_image").path())
    assert (
        valohai.inputs("single_image")
        .path(default="unused_default")
        .endswith("single_image/Example.jpg")
    )
    assert not valohai.inputs("nonono").path()
    assert valohai.inputs("nonono").path(default="default_123") == "default_123"
    assert os.path.exists(valohai.inputs("input_with_archive").path())
    for path in valohai.inputs("input_with_archive").paths():
        assert os.path.exists(path)
    assert len(list(valohai.inputs("input_with_archive").paths())) == 2


def test_get_input_streams(use_test_config_dir):
    assert valohai.inputs("single_image").stream().read(10000)
    assert len(list(valohai.inputs("input_with_archive").streams())) == 2
    for stream in valohai.inputs("input_with_archive").streams():
        assert stream.read(10000)
    assert valohai.inputs("single_image").stream().read()
    assert not valohai.inputs("nonono").stream()
