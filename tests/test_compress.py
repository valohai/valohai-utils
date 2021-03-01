import os
import tarfile
import zipfile

import pytest

import valohai


@pytest.mark.parametrize("format", ("zip", "tar", "tar.gz"))
@pytest.mark.parametrize("remove_originals", (False, True))
def test_compress(outputs_path, output_files, format, remove_originals):
    filename = "hello.{}".format(format)
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
