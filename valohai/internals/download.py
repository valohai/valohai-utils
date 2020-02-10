import os
import tempfile

from tqdm import tqdm


# TODO: This is close to valohai-local-run. Possibility to merge.
def download_url(url, path, force_download=False):
    if not os.path.isfile(path) or force_download:
        try:
            import requests
        except ImportError:
            raise RuntimeError(
                'The `requests` module must be available for download support (attempting to download %s)' % url
            )

        tmp_path = tempfile.NamedTemporaryFile().name
        print('Downloading %s -> %s' % (url, path))
        r = requests.get(url, stream=True)
        r.raise_for_status()
        total = (int(r.headers['content-length']) if 'content-length' in r.headers else None)

        t = tqdm(total=total, unit='iB', unit_scale=True)
        with open(tmp_path, 'wb') as f:
            for data in r.iter_content(1048576):
                t.update(len(data))
                f.write(data)
        t.close()
        os.replace(tmp_path, path)
    else:
        print('Using cached %s' % path)

    return path
