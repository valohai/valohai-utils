import os
import stat
from stat import S_IREAD, S_IRGRP, S_IROTH

import pytest

import valohai.outputs


def test_get_output_path(outputs_path):
    path = valohai.outputs.get_output_path("jahas.exe")
    assert path == os.path.join(outputs_path, "jahas.exe")
    assert os.path.isdir(os.path.dirname(path))

    path = valohai.outputs.get_output_path("herpderp/yomomma/joo.txt")

    assert path == os.path.join(outputs_path, "herpderp/yomomma/joo.txt")
    assert os.path.isdir(os.path.dirname(path))


def test_compress_zip(outputs_path, output_files):
    valohai.outputs.compress(output_files, "hello.zip")

    for path in output_files:
        assert not os.path.isfile(path)
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_compress_tar(outputs_path, output_files):
    valohai.outputs.compress(output_files, "hello.tar")

    for path in output_files:
        assert not os.path.isfile(path)
    assert os.path.isfile(os.path.join(outputs_path, "hello.tar"))


def test_compress_tar_gz(outputs_path, output_files):
    valohai.outputs.compress(output_files, "hello.tar.gz")

    for path in output_files:
        assert not os.path.isfile(path)
    assert os.path.isfile(os.path.join(outputs_path, "hello.tar.gz"))


def test_compress_multiple_folders(outputs_path, output_files):
    valohai.outputs.compress(["*", "folder", "folder2"], "hello.zip")

    for path in output_files:
        assert not os.path.isfile(path)
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_leave_originals(outputs_path, output_files):
    valohai.outputs.compress(output_files, "hello.zip", remove_originals=False)

    for path in output_files:
        assert os.path.isfile(path)
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_live_upload(outputs_path, output_files):
    valohai.outputs.compress(output_files, "hello.zip", live_upload=True)

    with pytest.raises(IOError):
        open(os.path.join(outputs_path, "hello.zip"), "w")
