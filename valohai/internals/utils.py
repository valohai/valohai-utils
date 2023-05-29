def uri_to_filename(uri: str) -> str:
    return uri.rpartition("/")[-1].split("?", 1)[0]


def string_to_bool(value: str) -> bool:
    if value.lower() == "false":
        return False
    return True


def get_sha256_hash(filepath: str) -> str:
    try:
        from valohai_cli.utils.hashing import get_fp_sha256
    except ImportError as ie:
        raise RuntimeError(
            "The `valohai-cli` module must be available " "for verifying hash"
        ) from ie

    with open(filepath, "rb") as f:
        return get_fp_sha256(f)  # type: ignore
