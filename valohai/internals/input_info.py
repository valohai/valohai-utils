import glob
import json
import os
from typing import Iterable, List, Optional, Union

from valohai import paths
from valohai.internals import global_state
from valohai.internals.download import download_url
from valohai.internals.download_type import DownloadType
from valohai.internals.utils import sift_default_value, uri_to_filename
from valohai.paths import get_inputs_path


class FileInfo:
    def __init__(
        self,
        *,
        name: str,
        uri: Optional[str],
        path: Optional[str],
        size: Optional[int],
        checksums: Optional[dict],
    ) -> None:
        self.name = str(name)
        self.uri = str(uri) if uri else None
        self.checksums = checksums
        self.path = str(path) if path else None
        self.size = int(size) if size else None

    def is_downloaded(self) -> Optional[bool]:
        return bool(self.path and os.path.isfile(self.path))

    def download(self, path: str, force_download: bool = False) -> None:
        if not self.uri:
            raise ValueError("Can not download file with no URI")
        self.path = download_url(
            self.uri, os.path.join(path, self.name), force_download
        )
        # TODO: Store size & checksums if they become useful


class InputInfo:
    def __init__(self, files: Iterable[FileInfo]):
        self.files = list(files)

    def is_downloaded(self) -> bool:
        if not self.files:
            return False

        return all(f.is_downloaded() for f in self.files)

    def download_if_necessary(
        self, name: str, download: DownloadType = DownloadType.OPTIONAL
    ):
        if (
            download == DownloadType.ALWAYS
            or not self.is_downloaded()
            and download == DownloadType.OPTIONAL
        ):
            path = get_inputs_path(name)
            os.makedirs(path, exist_ok=True)
            for f in self.files:
                f.download(path, (download == DownloadType.ALWAYS))

    @classmethod
    def from_json_data(cls, json_data: dict) -> "InputInfo":
        return cls(files=[FileInfo(**d) for d in json_data.get("files", ())])

    @classmethod
    def from_urls_and_paths(cls, urls_and_paths: Union[str, List]) -> "InputInfo":
        files = []

        if not isinstance(urls_and_paths, list):
            urls_and_paths = [urls_and_paths]

        for value in urls_and_paths:
            if "://" not in value:  # The string is a local path
                for path in glob.glob(value):
                    files.append(
                        FileInfo(
                            name=os.path.basename(path),
                            uri=None,
                            path=value,
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


def get_input_info(
    name: str,
    download: DownloadType = DownloadType.OPTIONAL,
    default: Union[str, List[str]] = None,
) -> Optional[InputInfo]:

    if name in global_state.inputs_cache:
        return global_state.inputs_cache[name]

    result = find_input_info(name)

    if result is None and default is not None:
        result = InputInfo.from_urls_and_paths(default)

    if result:
        result.download_if_necessary(name, download)
        global_state.inputs_cache[name] = result

    return result


def find_input_info(
    name: str,
) -> Optional[InputInfo]:
    """Find the InputInfo for a given input name.

    The InputInfo can be loaded from various sources (in the order of priority):
    1. Command-line argument
    2. inputs.json Valohai config
    3. default_inputs from valohai.prepare()

    :param name: Name of the input.
    :return: InputInfo instance for this input name
    """

    # Option 1: Command-line argument
    if name in global_state.parsed_cli_inputs:
        parsed_cli_input = global_state.parsed_cli_inputs[name]
        return InputInfo.from_urls_and_paths(parsed_cli_input)

    # Option 2: inputs.json Valohai config
    elif os.path.isfile(paths.get_inputs_config_path()):
        with open(paths.get_inputs_config_path()) as json_file:
            data = json.load(json_file)
            input_info_data = data.get(name)
            if input_info_data:
                return InputInfo.from_json_data(input_info_data)

    # Option 3: default_inputs from valohai.prepare()
    elif name in global_state.default_inputs:
        default_value = sift_default_value(name, global_state.default_inputs[name])
        return InputInfo.from_urls_and_paths(default_value)

    return None
