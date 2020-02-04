import glob
import os
import tarfile
import tempfile
import zipfile

from valohai.internals.files import get_compressed_file_suffix, set_file_read_only, get_glob_pattern
from valohai.paths import get_outputs_path


def compress(source: str, target: str, live_upload: bool = False, remove_originals: bool = True):
    """Compress output files as single package.

    Compresses files into temporary file, which is then copied to the target path. Optionally removes original
    files and live uploads the package.

    :param source: Things to compress. Supports wildcard and directory name. (examples: "folder", "folder/*.jpg")
    :param target: Name of the compressed file. Suffix is used to determine compression type ("example.zip")
    :param live_upload: Is the resulting package live uploaded to data store (cloud execution only)
    :param remove_originals: Are the original files removed after packaging

    """
    source_path = get_outputs_path(source, auto_create=False)
    target_path = get_outputs_path(target)

    suffix = get_compressed_file_suffix(target)
    tmp_path = tempfile.NamedTemporaryFile(suffix=suffix).name

    if suffix == ".zip":
        target_file = zipfile.ZipFile(tmp_path, mode='w')
    elif suffix == ".tar.gz":
        target_file = tarfile.open(tmp_path, "w:gz")

    try:
        compressed_paths = []
        for file_path in glob.glob(get_glob_pattern(source_path)):
            if suffix == ".zip":
                target_file.write(file_path)
            elif suffix == ".tar.gz":
                target_file.add(file_path)
            compressed_paths.append(file_path)
    finally:
        target_file.close()

    if compressed_paths:
        os.replace(tmp_path, target_path)
        if remove_originals:
            for file_path in compressed_paths:
                os.remove(file_path)

        if live_upload:
            set_file_read_only(target_path)
    else:
        raise ValueError("No files to compress at %s" % source_path)


def live_upload(source: str):
    for file_path in glob.glob(get_glob_pattern(source)):
        set_file_read_only(file_path)

