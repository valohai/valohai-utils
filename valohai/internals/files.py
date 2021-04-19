import glob
import os
import pathlib
from stat import S_IREAD, S_IRGRP, S_IROTH
from typing import Set, Union


def set_file_read_only(path: str) -> None:
    os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)


def get_glob_pattern(source: str) -> str:
    # Path is transformed into glob supported pattern. "example" -> "example/*"
    if os.path.isdir(source):
        return f"{source.rstrip('/')}/*"
    return source


def expand_globs(sources: Union[str, list], preprocessor=lambda s: s) -> Set[str]:
    if isinstance(sources, str):
        sources = [sources]
    files_to_compress = set()
    for source_path in sources:
        source_path = preprocessor(source_path)
        glob_pattern = get_glob_pattern(source_path)
        for file_path in glob.glob(glob_pattern):
            if os.path.isfile(file_path):
                files_to_compress.add(file_path)
    if not files_to_compress:
        raise ValueError(f"No files to compress at {sources}")
    return files_to_compress


def get_canonical_extension(pathname: str) -> str:
    """
    Get a canonicalized extension from a pathname. Correctly handles e.g. `tar.gz`.
    """
    return "".join(pathlib.Path(pathname).suffixes).lower()
