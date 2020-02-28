import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from typing import Iterable, List, Union


def set_file_read_only(path: str):
    os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)


def get_glob_pattern(source: str) -> str:
    # Path is transformed into glob supported pattern. "example" -> "example/*"
    if os.path.isdir(source):
        source = "%s/*" % source.rstrip('/')
    return source


def expand_files(sources: Union[str, List[str]]) -> Iterable[str]:
    seen = set()
