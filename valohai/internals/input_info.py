import glob
import os
from typing import Any, Dict, Iterable, List, Optional, Union

from valohai_yaml.utils import listify

from valohai.internals.download import download_url, request_download_urls
from valohai.internals.download_type import DownloadType
from valohai.internals.utils import uri_to_filename
from valohai.paths import get_inputs_path


class FileInfo:
    def __init__(
        self,
        *,
        name: str,
        uri: Optional[str] = None,
        path: Optional[str] = None,
        size: Optional[int] = None,
        checksums: Optional[Dict[str, str]] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
        datum_id: Optional[str] = None,
    ) -> None:
        self.name = str(name)
        self.uri = str(uri) if uri else None
        self.download_url = self.uri
        self.checksums = dict(checksums) if checksums else {}
        self.path = str(path) if path else None
        self.size = int(size) if size else None
        self.metadata = list(metadata) if metadata else []
        self.datum_id = str(datum_id) if datum_id else None

    def is_downloaded(self) -> Optional[bool]:
        return bool(self.path and os.path.isfile(self.path))

    def download(self, path: str, force_download: bool = False) -> None:
        if not self.download_url:
            raise ValueError("Can not download file with no URI")
        self.path = download_url(
            self.download_url, os.path.join(path, self.name), force_download
        )
        # TODO: Store size & checksums if they become useful

    @classmethod
    def from_json_data(cls, json_data: Dict[str, Any]) -> "FileInfo":
        return cls(
            name=json_data["name"],
            uri=json_data.get("uri"),
            path=json_data.get("path"),
            size=json_data.get("size"),
            checksums=json_data.get("checksums"),
            metadata=json_data.get("metadata"),
            datum_id=json_data.get("datum_id"),
        )


class InputInfo:
    def __init__(self, files: Iterable[FileInfo], input_id: Optional[str] = None):
        self.files = list(files)
        self.input_id = input_id

    def is_downloaded(self) -> bool:
        if not self.files:
            return False

        return all(f.is_downloaded() for f in self.files)

    def download_if_necessary(
        self, name: str, download: DownloadType = DownloadType.OPTIONAL
    ) -> None:
        if (
            download == DownloadType.ALWAYS
            or not self.is_downloaded()
            and download == DownloadType.OPTIONAL
        ):
            path = get_inputs_path(name)
            os.makedirs(path, exist_ok=True)
            if self.input_id:
                # Resolve download URLs from Valohai before downloading
                filenames_to_urls = request_download_urls(self.input_id)
                for file in self.files:
                    if not file.is_downloaded():
                        file.download_url = filenames_to_urls[file.name]
            for f in self.files:
                f.download(path, force_download=(download == DownloadType.ALWAYS))

    @classmethod
    def from_json_data(cls, json_data: Dict[str, Any]) -> "InputInfo":
        return cls(
            input_id=json_data.get("input_id"),
            files=[FileInfo.from_json_data(d) for d in json_data.get("files", ())],
        )

    @classmethod
    def from_urls_and_paths(cls, urls_and_paths: Union[str, List[str]]) -> "InputInfo":
        files = []

        for value in listify(urls_and_paths):
            # TODO: this cast shouldn't be required,
            #       but listify()'s types are wonky with new mypy
            value = str(value)
            if "://" not in value:  # The string is a local path
                for path in glob.glob(value):
                    files.append(
                        FileInfo(
                            name=os.path.basename(path),
                            uri=None,
                            path=path,
                            size=None,
                            checksums=None,
                        )
                    )
            else:  # The string is an URL
                files.append(
                    FileInfo(
                        name=uri_to_filename(value),
                        uri=value,
                        path=None,
                        size=None,
                        checksums=None,
                    )
                )

        return cls(files=files)
