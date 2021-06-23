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

    assert (
        valohai.inputs("single_image")
        .path("Example.jpg")
        .endswith("single_image/Example.jpg")
    )
    assert (
        valohai.inputs("single_image")
        .path("*.jpg")
        .endswith("single_image/Example.jpg")
    )
    assert (
        valohai.inputs("single_image").path("E*").endswith("single_image/Example.jpg")
    )
    assert valohai.inputs("single_image").path("*").endswith("single_image/Example.jpg")
    assert not valohai.inputs("single_image").path("notbefound*")
    assert next(valohai.inputs("single_image").paths("Example.jpg")).endswith(
        "single_image/Example.jpg"
    )
    assert next(valohai.inputs("single_image").paths("*.jpg")).endswith(
        "single_image/Example.jpg"
    )
    assert next(valohai.inputs("single_image").paths("E*")).endswith(
        "single_image/Example.jpg"
    )
    assert next(valohai.inputs("single_image").paths("*")).endswith(
        "single_image/Example.jpg"
    )
    assert len(list(valohai.inputs("single_image").paths("notbefound*"))) == 0

    assert not valohai.inputs("nonono").path()
    assert valohai.inputs("nonono").path(default="default_123") == "default_123"
    assert os.path.exists(valohai.inputs("input_with_archive").path())
    assert len(list(valohai.inputs("input_with_archive").paths())) == 5
    assert len(list(valohai.inputs("input_with_archive").paths("**/*.txt"))) == 2
    assert len(list(valohai.inputs("input_with_archive").paths("**/a*.jpg"))) == 1
    assert next(valohai.inputs("input_with_archive").paths("**/a*.jpg")).endswith(
        "blerp/blonk/asdf.jpg"
    )
    assert next(valohai.inputs("input_with_archive").paths("**/asdf.jpg")).endswith(
        "blerp/blonk/asdf.jpg"
    )
    assert next(
        valohai.inputs("input_with_archive").paths("blerp/blonk/asdf.jpg")
    ).endswith("blerp/blonk/asdf.jpg")

    for path in valohai.inputs("input_with_archive").paths():
        assert os.path.exists(path)

    assert len(list(valohai.inputs("input_with_archive").paths())) == 5

    for path in valohai.inputs("input_with_archive").paths("**/*.jpg"):
        assert os.path.exists(path)

    assert next(
        valohai.inputs("images_in_subdirs").paths("hello/label1/hello/*.jpg")
    ).endswith("label1/hello/foo.jpg")
    assert next(
        valohai.inputs("images_in_subdirs").paths("hello/label2/hello/*.jpg")
    ).endswith("label2/hello/foo.jpg")
    assert (
        len(list(valohai.inputs("images_in_subdirs").paths("hello/**/hello/*.jpg")))
        == 2
    )
    assert len(list(valohai.inputs("images_in_subdirs").paths("hello/**/*.jpg"))) == 2
    assert len(list(valohai.inputs("images_in_subdirs").paths("**/*.jpg"))) == 2
    for path in valohai.inputs("images_in_subdirs").paths("**/*.jpg"):
        assert os.path.exists(path)


def test_get_input_streams(use_test_config_dir):
    assert valohai.inputs("single_image").stream().read(10000)
    assert len(list(valohai.inputs("input_with_archive").streams())) == 5

    for stream in valohai.inputs("input_with_archive").streams():
        assert stream.read(10000)
    assert valohai.inputs("single_image").stream().read()
    assert not valohai.inputs("nonono").stream()
    assert (
        len(list(valohai.inputs("images_in_subdirs").streams("hello/**/hello/*.jpg")))
        == 2
    )
    assert len(list(valohai.inputs("images_in_subdirs").streams("hello/**/*.jpg"))) == 2
    assert len(list(valohai.inputs("images_in_subdirs").streams("**/*.jpg"))) == 2
    for stream in valohai.inputs("images_in_subdirs").streams("**/*.jpg"):
        assert stream.read(10000)


def test_zip_no_mangling(use_test_config_dir):
    paths = set(valohai.inputs("input_with_archive").paths())
    for suffix in (
        "1hello.txt",
        "2world.txt",
        "blerp/3katt.txt",
        "blerp/blonk/4blöf.txt",
        "blerp/blonk/asdf.jpg",
    ):
        assert any(p.endswith(suffix) for p in paths)
