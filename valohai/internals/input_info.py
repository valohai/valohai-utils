import os

from valohai.internals.download import download_url


class FileInfo:
    def __init__(self, *, name, uri, path, size, checksums):
        self.name = str(name)
        self.uri = str(uri)
        self.checksums = checksums
        self.path = str(path) if path else None
        self.size = int(size) if size else None

    def is_downloaded(self):
        return self.path and os.path.isfile(self.path)

    def download(self, path, force_download: bool = False):
        self.path = download_url(self.uri, os.path.join(path, self.name), force_download)
        # TODO: Store size & checksums if they become useful


class InputInfo:
    def __init__(self, files):
        self.files = list(files)

    def is_downloaded(self):
        if not self.files:
            return False

        return all(f.is_downloaded() for f in self.files)

    def download(self, path, force_download: bool = False):
        for f in self.files:
            f.download(path, force_download)


    @classmethod
    def from_json_data(cls, json_data: dict) -> "InputInfo":
        return cls(files=[FileInfo(**d) for d in json_data.get("files", ())])
