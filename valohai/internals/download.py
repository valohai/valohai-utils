import os
import tempfile


# TODO: This is close to valohai-local-run. Possibility to merge.
def download_url(url: str, path: str, force_download: bool = False) -> str:
    if not os.path.isfile(path) or force_download:
        try:
            import requests
            from tqdm import tqdm
        except ImportError as ie:
            raise RuntimeError(
                "The `requests` and `tqdm` modules must be available "
                "for download support (attempting to download %s)" % url
            ) from ie

        tmp_path = tempfile.NamedTemporaryFile().name
        print(f"Downloading {url} -> {path}")  # noqa
        r = requests.get(url, stream=True)
        r.raise_for_status()
        total = (
            int(r.headers["content-length"]) if "content-length" in r.headers else None
        )

        with tqdm(total=total, unit="iB", unit_scale=True) as t, open(
            tmp_path, "wb"
        ) as f:
            for data in r.iter_content(1048576):
                t.update(len(data))
                f.write(data)
        os.replace(tmp_path, path)
    else:
        print(f"Using cached {path}")  # noqa

    return path
