import glob
import os
import tarfile
import tempfile
import zipfile
from typing import Union

from valohai.internals.files import get_compressed_file_suffix, set_file_read_only, get_glob_pattern
from valohai.paths import get_output_path


def compress(source: Union[str, list], target: str, live_upload: bool = False, remove_originals: bool = True):
    """Compress output files as single package.

    Compresses files into temporary file, which is then copied to the target path. Optionally removes original
    files and live uploads the package.

    :param source: List of things to compress. Supports wildcard(s) and directory name(s). (examples: "folder", "folder/*.jpg")
    :param target: Name of the compressed file. Suffix is used to determine compression type ("example.zip")
    :param live_upload: Sets the result file read-only to allow live upload in cloud executions
    :param remove_originals: Are the original files removed after packaging

    """

    if isinstance(source, str):
        source = [source]

    target_path = get_output_path(target)
    suffix = get_compressed_file_suffix(target)
    tmp_path = tempfile.NamedTemporaryFile(suffix=suffix).name

    with _open_new_archive(tmp_path, suffix) as target_file:
        compressed_paths = []
        for source_path in source:
            source_path = get_output_path(source_path, auto_create=False)
            glob_pattern = get_glob_pattern(source_path)
            for file_path in glob.glob(glob_pattern):
                if os.path.isfile(file_path):
                    if suffix == ".zip":
                        compress_type = zipfile.ZIP_STORED if file_path.endswith(".zip") else zipfile.ZIP_DEFLATED
                        target_file.write(file_path, compress_type=compress_type)
                    elif suffix == ".tar" or suffix == ".tar.gz":
                        target_file.add(file_path)
                    compressed_paths.append(file_path)

        if compressed_paths:
            os.replace(tmp_path, target_path)
            if remove_originals:
                for file_path in compressed_paths:
                    os.remove(file_path)

            if live_upload:
                set_file_read_only(target_path)
        else:
            raise ValueError("No files to compress at %s" % source_path)


def _open_new_archive(path: str, suffix: str):
    if suffix == ".zip":
        return zipfile.ZipFile(path, mode='w')
    elif suffix == ".tar":
        return tarfile.open(path, "w")
    elif suffix == ".tar.gz":
        return tarfile.open(path, "w:gz")


def live_upload(source: str):
    for file_path in glob.glob(get_glob_pattern(source)):
        set_file_read_only(file_path)

