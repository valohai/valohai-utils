import contextlib
import os
import tempfile


# TODO: This is close to valohai-local-run. Possibility to merge.
def download_url(url: str, path: str, force_download: bool = False) -> str:
    if not os.path.isfile(path) or force_download:
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
