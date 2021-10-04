import os
import tarfile
import zipfile

import pytest

import valohai
from tests.conftest import create_files


@pytest.mark.parametrize("format", ("zip", "tar", "tar.gz"))
@pytest.mark.parametrize("remove_originals", (False, True))
def test_compress(output_files, format, remove_originals):
    filename = f"hello.{format}"
    package_path = valohai.outputs("morjes").compress(
        output_files, filename, remove_originals=remove_originals
    )

    for path in output_files:
        assert os.path.isfile(path) != remove_originals

    # Quick format smoke checks.
    if format == "zip":
        with zipfile.ZipFile(package_path) as zf:
            assert zf.namelist()
    elif "tar" in format:
        with tarfile.open(package_path, "r:*") as tf:
            assert len(list(tf))


@pytest.mark.parametrize("format", ("zip", "tar", "tar.gz"))
@pytest.mark.parametrize("remove_originals", (False, True))
@pytest.mark.parametrize("filter, expected_files", [("**", 6), ("**/*.jpg", 2)])
def test_compress_wildcards(tmpdir, format, remove_originals, filter, expected_files):
    source_dir = tmpdir.strpath
    created_files = create_files(source_dir)

    filename = f"hello.{format}"
    package_path = valohai.outputs("foo").compress(
        source=os.path.join(source_dir, filter),
        filename=filename,
        remove_originals=remove_originals,
    )

    for path in created_files:
        # picture.jpg should be always compressed with our filter(s)
        if "picture.jpg" in path:
            assert os.path.isfile(path) != remove_originals

    if format == "zip":
        with zipfile.ZipFile(package_path) as zf:
            assert len(zf.namelist()) == expected_files
            # picture.jpg should be always compressed with our filter(s)
            assert "folder/picture.jpg" in zf.namelist()
    elif "tar" in format:
        with tarfile.open(package_path, "r:*") as tf:
            assert len(list(tf)) == expected_files
            # picture.jpg should be always compressed with our filter(s)
            assert "folder/picture.jpg" in [tarinfo.name for tarinfo in list(tf)]
