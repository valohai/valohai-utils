import contextlib
import os
import tempfile
from typing import Any

from requests import Response
from valohai.internals.utils import uri_to_filename, get_sha256_hash


# TODO: This is close to valohai-local-run. Possibility to merge.
def resolve_datum(datum_id: str) -> Dict[str, Any]:
    try:
        from valohai_cli.api import request  # type: ignore
    except ImportError as ie:
        raise RuntimeError("Can't resolve datum without valohai-cli") from ie
    resp: Response = request(url=f"/api/v0/data/{datum_id}", method="GET")
    resp.raise_for_status()
    return resp.json()


def verify_datum(datum_obj: Dict[str, Any], input_folder_path: str) -> str:
    filename = datum_obj["name"]
    checksums = {
        "md5": datum_obj["md5"],
        "sha1": datum_obj["sha1"],
        "sha256": datum_obj["sha256"],
    }
    file_path = os.path.join(input_folder_path, filename)
    if filename in os.listdir(input_folder_path) and checksums[
        "sha256"
    ] == get_sha256_hash(file_path):
        return file_path
    raise Exception(
        "Datum details are not matched with"
        " locally available file. Either the name or content of local file is altered."
    )


def download_url(url: str, path: str, force_download: bool = False) -> str:
    if not os.path.isfile(path) or force_download:
        if url.startswith("datum://"):
            input_folder_path = os.path.dirname(path)
            response = resolve_datum(uri_to_filename(url))
            path = verify_datum(response, input_folder_path)
        else:
            _do_download(url, path)
    else:
        print(f"Using cached {path}")  # noqa

    return path


def _do_download(url: str, path: str) -> None:
    try:
        import requests
    except ImportError as ie:
        raise RuntimeError(
            f"The `requests` module must be available for download support (attempting to download {url})"
        ) from ie

    tmp_path = tempfile.NamedTemporaryFile().name
    print(f"Downloading {url} -> {path}")  # noqa
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total = int(r.headers["content-length"]) if "content-length" in r.headers else None
    try:
        from tqdm import tqdm

        prog = tqdm(total=total, unit="iB", unit_scale=True)
    except ImportError:
        prog = contextlib.nullcontext()

    with prog, open(tmp_path, "wb") as f:
        for chunk in r.iter_content(1048576):
            if prog:
                prog.update(len(chunk))
            f.write(chunk)
    os.replace(tmp_path, path)
