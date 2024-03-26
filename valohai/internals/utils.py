from typing import List, Callable, Optional


def uri_to_filename(uri: str) -> str:
    return uri.rpartition("/")[-1].split("?", 1)[0]


def string_to_bool(value: str) -> bool:
    if value.lower() == "false":
        return False
    return True


def get_sha256_hash(filepath: str) -> str:
    try:
        from valohai_cli.utils.hashing import get_fp_sha256  # type: ignore
    except ImportError as ie:
        raise RuntimeError(
            "The `valohai-cli` module must be available for verifying hash"
        ) from ie

    with open(filepath, "rb") as f:
        return get_fp_sha256(f)  # type: ignore


def is_local_file_path(path_str: str) -> bool:
    if "://" in path_str:
        return False
    return True


def string_to_list_separated_by_separator(
    separator: Optional[str] = None,
) -> Callable[[str], List[str]]:
    if not separator:
        separator = ","

    def string_to_separated_list(value: str) -> List[str]:
        return value.split(separator)

    return string_to_separated_list
