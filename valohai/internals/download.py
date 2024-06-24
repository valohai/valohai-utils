import contextlib
import os
import tempfile
from typing import Any, Dict, Union

from requests import Response
from valohai.internals.utils import uri_to_filename, get_sha256_hash


def resolve_datum(datum_id: str) -> Dict[str, Any]:
    datum_id_or_alias = datum_id
    try:
        from valohai_cli.api import request  # type: ignore
    except ImportError as ie:
        raise RuntimeError("Can't resolve datum without valohai-cli") from ie

    try:
        from uuid import UUID

        UUID(datum_id_or_alias, version=4)
        resp: Response = request(url=f"/api/v0/data/{datum_id_or_alias}", method="GET")
        resp.raise_for_status()
        data = resp.json()
    except ValueError:
        from valohai_cli.settings import settings

        project = settings.get_project(".")
        if project is None:
            raise RuntimeError(
                f"Can't resolve datum alias '{datum_id_or_alias}' without a project"
                ", linked by valohai-cli"
            )
        resp: Response = request(
            url=f"/api/v0/datum-aliases/resolve/?name={datum_id_or_alias}&project={project.id}",
            method="GET",
        )
        resp.raise_for_status()
        data = resp.json()["datum"]

    assert isinstance(data, dict)
    return data


def verify_datum(
    datum_obj: Dict[str, Any],
    input_folder_path: Union[str, None] = None,
    *,
    file_path: Union[str, None] = None,
) -> str:
    if input_folder_path is not None:
        filename = datum_obj["name"]
        file_path = os.path.join(input_folder_path, filename)
    if input_folder_path is None and file_path is None:
        raise ValueError(
            "either input folder path or file path (keyword-only argument) must be given"
        )
    if os.path.exists(file_path) and datum_obj["sha256"] == get_sha256_hash(file_path):
        return file_path
    raise Exception(
        f"The local file {file_path!r} does not exist, "
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
        prog = contextlib.nullcontext()

    with prog as prog, open(tmp_path, "wb") as f:
        for chunk in r.iter_content(1048576):
            if prog:
                prog.update(len(chunk))
            f.write(chunk)
    os.replace(tmp_path, path)
