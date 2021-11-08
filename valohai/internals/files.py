import glob
import os
import pathlib
from stat import S_IREAD, S_IRGRP, S_IROTH
from typing import Callable, List, Set, Tuple, Union

from valohai_yaml.utils import listify


def set_file_read_only(path: str) -> None:
    os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)


def get_glob_pattern(source: str) -> str:
    # Path is transformed into glob supported pattern. "example" -> "example/*"
    if os.path.isdir(source):
        return f"{source.rstrip('/')}/*"
    return source


def expand_globs(
    sources: Union[str, List[str]], preprocessor: Callable[[str], str] = lambda s: s
) -> Set[Tuple[str, str]]:
    """Returns a set of paths as a result of expanding all the source wildcards

    First item of the resulting tuple item is the expanded path
    Second item of the resulting tuple is the logical root path

    Example
    source: /tmp/foo/**/*.png
    output: set(("/tmp/foo/bar/hello.png", "/tmp/foo"), ("/tmp/foo/bar/sub/jello.png", "/tmp/foo"))

    source: /tmp/yeah/*.png
    output: set(("/tmp/yeah/hello.png", "/tmp/yeah"), ("/tmp/yeah/jello.png", "/tmp/yeah"))

    :param sources: Path or list of paths. May contain * or ** wildcards.
    :param preprocessor: Preprocessor to be used for each of the paths
    :return:
    """

    sources = listify(sources)
    files_to_compress = set()
    for source_path in sources:
        source_path = preprocessor(source_path)
        glob_pattern = get_glob_pattern(source_path)
        root_path = os.path.dirname(glob_pattern).split("*", 1)[0]  # Handles ** also
        for file_path in glob.glob(glob_pattern, recursive=True):
            if os.path.isfile(file_path):
                files_to_compress.add((file_path, root_path))
    if not files_to_compress:
        raise ValueError(f"No files to compress at {sources}")
    return files_to_compress


def get_canonical_extension(pathname: str) -> str:
    """
    Get a canonicalized extension from a pathname. Correctly handles e.g. `tar.gz`.
    """
    return "".join(pathlib.Path(pathname).suffixes).lower()
