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
    assert len(list(valohai.inputs("input_with_archive").paths())) == 4


def test_get_input_streams(use_test_config_dir):
    assert valohai.inputs("single_image").stream().read(10000)
    assert len(list(valohai.inputs("input_with_archive").streams())) == 4
    for stream in valohai.inputs("input_with_archive").streams():
        assert stream.read(10000)
    assert valohai.inputs("single_image").stream().read()
    assert not valohai.inputs("nonono").stream()


def test_zip_no_mangling(use_test_config_dir):
    paths = set(valohai.inputs("input_with_archive").paths())
    for suffix in (
        "1hello.txt",
        "2world.txt",
        "blerp/3katt.txt",
        "blerp/blonk/4blöf.txt",
    ):
        assert any(p.endswith(suffix) for p in paths)
