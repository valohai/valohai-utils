from stat import S_IREAD, S_IRGRP, S_IROTH
import os


def set_file_read_only(path: str):
    if os.path.exists(path):
        os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)
    else:
        raise ValueError("Path %s doesn't exist!" % path)


def get_compressed_file_suffix(path: str) -> str:
    if path.endswith(".zip"):
        return ".zip"
    elif path.endswith(".tar.gz"):
        return ".tar.gz"
    else:
        raise ValueError("Unrecognized compression format. Please use .zip or .tar.gz")


def get_glob_pattern(source: str) -> str:
    # Path is transformed into glob supported pattern. "example" -> "example/*"
    if os.path.isdir(source):
        source = "%s/*" % source.rstrip('/')
    return source
