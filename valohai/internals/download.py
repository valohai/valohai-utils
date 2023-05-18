import os
import tempfile
from valohai.internals.utils import uri_to_filename, check_sha256_hashing


# TODO: This is close to valohai-local-run. Possibility to merge.
def resolve_datum(datum_id: str) -> ...:
    try:
        from valohai_cli.api import request
    except ImportError as ie:
        raise RuntimeError("Can't resolve datum without valohai-cli") from ie
    resp = request(url=f"/api/v0/data/{datum_id}", method="GET", stream=True)
    resp.raise_for_status()
    return resp


def verify_datum(response: any, input_folder_path: str) -> str:
    datum_obj = response.json()
    filename = datum_obj['name']
    checksums = {'md5': datum_obj['md5'],
                 'sha1': datum_obj['sha1'],
                 'sha256': datum_obj['sha256']}
    file_path = os.path.join(input_folder_path, filename)
    if filename in os.listdir(input_folder_path) \
            and checksums['sha256'] == check_sha256_hashing(file_path):
        return os.path.join(input_folder_path, filename)
    else:
        raise Exception(f"Datum details (name or content) are not matched with"
                        f" locally available file. Please check again.")


def download_url(url: str, path: str, force_download: bool = False) -> str:
    if not os.path.isfile(path) or force_download:
        try:
            import requests
            from tqdm import tqdm
        except ImportError as ie:
            raise RuntimeError(
                f"The `requests` and `tqdm` modules must be available "
                f"for download support (attempting to download {url})"
            ) from ie

        if "datum://" in url:
            print("Fetching datum details....", path)
            input_folder_path = path.rsplit('/', 1)[0]  # getting folder path only
            response = resolve_datum(uri_to_filename(url))
            if response.status_code == 200:
                path = verify_datum(response, input_folder_path)
            else:
                raise Exception(f"Failed to resolve: {uri_to_filename(url)}, Error code: {resp.status_code}")
        else:
            # force download new file
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
