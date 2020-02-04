import os
import stat
from stat import S_IREAD, S_IRGRP, S_IROTH

import valohai.outputs


def test_get_output_path(outputs_path):
    path = valohai.outputs.get_outputs_path("jahas.exe")
    assert path == os.path.join(outputs_path, "jahas.exe")
    assert os.path.isdir(os.path.dirname(path))

    path = valohai.outputs.get_outputs_path("herpderp/yomomma/joo.txt")

    assert path == os.path.join(outputs_path, "herpderp/yomomma/joo.txt")
    assert os.path.isdir(os.path.dirname(path))


def test_compress_zip(outputs_path, output_files):
    assert os.path.isfile(output_files[0])

    valohai.outputs.compress(output_files[0], "hello.zip")

    assert not os.path.isfile(output_files[0])
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_compress_tar(outputs_path, output_files):
    assert os.path.isfile(output_files[0])

    valohai.outputs.compress(output_files[0], "hello.tar.gz")

    assert not os.path.isfile(output_files[0])
    assert os.path.isfile(os.path.join(outputs_path, "hello.tar.gz"))


def test_compress_folder(outputs_path, output_files):
    assert os.path.isfile(output_files[2])
    assert os.path.isfile(output_files[3])
    assert os.path.isfile(output_files[4])

    valohai.outputs.compress("folder", "hello.zip")

    assert not os.path.isfile(output_files[2])
    assert not os.path.isfile(output_files[3])
    assert not os.path.isfile(output_files[4])
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_compress_folder_with_wildcard(outputs_path, output_files):
    assert os.path.isfile(output_files[2])
    assert os.path.isfile(output_files[3])
    assert os.path.isfile(output_files[4])

    valohai.outputs.compress("folder/*.jpg", "hello.zip")

    assert not os.path.isfile(output_files[2])
    assert not os.path.isfile(output_files[3])
    assert os.path.isfile(output_files[4])
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_leave_originals(outputs_path, output_files):
    assert os.path.isfile(output_files[0])

    valohai.outputs.compress(output_files[0], "hello.zip", remove_originals=False)

    assert os.path.isfile(output_files[0])
    assert os.path.isfile(os.path.join(outputs_path, "hello.zip"))


def test_live_upload(outputs_path, output_files):
    assert os.path.isfile(output_files[0])

    valohai.outputs.compress(output_files[0], "hello.zip", live_upload=True)
    valohai.outputs.compress(output_files[1], "hello2.zip", live_upload=False)

    zip_path1 = os.path.join(outputs_path, "hello.zip")
    zip_path2 = os.path.join(outputs_path, "hello2.zip")

    assert stat.S_IMODE(os.lstat(zip_path1).st_mode) == S_IREAD | S_IRGRP | S_IROTH
    assert stat.S_IMODE(os.lstat(zip_path2).st_mode) != S_IREAD | S_IRGRP | S_IROTH
