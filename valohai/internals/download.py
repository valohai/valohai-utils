import contextlib
import os
import tempfile
import shutil
from typing import Any, Dict, Union

from requests import Response
from valohai.internals.utils import uri_to_filename, get_sha256_hash
from valohai.internals.api_calls import send_api_request


def resolve_datum(datum_id: str) -> Dict[str, Any]:
    datum_id_or_alias = datum_id
    try:
        from valohai_cli.api import request  # type: ignore
    except ImportError as ie:
        raise RuntimeError("Can't resolve datum without valohai-cli") from ie

    try:
        from uuid import UUID

        UUID(datum_id_or_alias, version=4)
        resp_by_id: Response = request(
            url=f"/api/v0/data/{datum_id_or_alias}", method="GET"
        )
        resp_by_id.raise_for_status()
        data = resp_by_id.json()
    except ValueError:
        from valohai_cli.settings import settings  # type: ignore

        project = settings.get_project(".")
        if project is None:
            raise RuntimeError(
                f"Can't resolve datum alias '{datum_id_or_alias}' without a project"
                ", linked by valohai-cli"
            )
        resp_by_alias: Response = request(
            url=f"/api/v0/datum-aliases/resolve/?name={datum_id_or_alias}&project={project.id}",
            method="GET",
        )
        resp_by_alias.raise_for_status()
        data = resp_by_alias.json()["datum"]

    assert isinstance(data, dict)
    return data


def verify_datum(
    datum_obj: Dict[str, Any],
    input_folder_path: Union[str, None] = None,
    *,
    file_path: Union[str, None] = None,
) -> str:
    datum_file_path: str
    if input_folder_path is not None:
        filename = datum_obj["name"]
        datum_file_path = str(os.path.join(input_folder_path, filename))
    elif file_path is not None:
        datum_file_path = file_path
    else:
        raise ValueError(
            "either input folder path or file path (keyword-only argument) must be given"
        )
    if os.path.exists(datum_file_path) and datum_obj["sha256"] == get_sha256_hash(
        datum_file_path
    ):
        return datum_file_path
    raise Exception(
        f"The local file {datum_file_path!r} does not exist, "
        f"or its checksum does not match with datum {datum_obj['id']}."
    )


# TODO: This is close to valohai-local-run. Possibility to merge.
def download_url(url: str, path: str, force_download: bool = False) -> str:
    if not os.path.isfile(path) or force_download:
        if url.startswith("datum://"):
            input_folder_path = os.path.dirname(path)
            datum_id_or_alias = uri_to_filename(url)
            datum_obj = resolve_datum(datum_id_or_alias)
            filename = datum_obj["name"]
            file_path = os.path.join(input_folder_path, filename)

            # it's safe to import valohai_cli, because resolve_datum bails out if it is not available
            from valohai_cli.api import request

            download_response = request(
                url=f"/api/v0/data/{datum_obj['id']}/download/", method="GET"
            )
            download_response.raise_for_status()
            _do_download(download_response.json()["url"], file_path)

            path = verify_datum(datum_obj, file_path=file_path)
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
        prog = contextlib.nullcontext()  # type: ignore

    with prog as prog, open(tmp_path, "wb") as f:
        for chunk in r.iter_content(1048576):
            if prog:
                prog.update(len(chunk))
            f.write(chunk)
    try:
        os.replace(tmp_path, path)
    except OSError:
        # different filesystems, for example a tmp filesystem, Docker volume, etc
        if os.path.isfile(path):
            os.remove(path)
        shutil.copy(tmp_path, path)


def request_download_urls(input_id: str) -> Dict[str, str]:
    """Request download URLs for the input from Valohai.

    Returns a dict of filename -> download URL for the given input.
    """
    try:
        import requests
    except ImportError as ie:
        raise RuntimeError("Can't download on demand without requests") from ie

    try:
        response = send_api_request(
            endpoint="input_request", params={"inputs": [input_id]}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError("Could not get new input download URLs") from e

    # While we should only get the single input we request in the response, this does handle the case
    # that we also get unrelated inputs.
    return dict(
        (input_file["filename"], input_file["url"])
        for input_request in response.json()
        for input_file in input_request["files"]
        if input_file["input_id"] == input_id
    )
