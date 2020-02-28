import json
import os

from typing import IO, Iterable, List, Optional

from valohai.internals.download_type import DownloadType
from valohai.internals.global_state import inputs
from valohai.paths import get_inputs_path
from . import paths
from .internals import vfs
from .internals.input_info import InputInfo


def get_input_paths(name: str, default: Optional[List[str]] = None, force_download: bool = False) -> Optional[List[str]]:
    """Get paths to all files for a given input name.

    Returns a list of file system paths for an input.
    If the file(s) are not found in the cache, they are downloaded automatically.

    See get_input_file_paths() or get_input_file_streams() for higher level alternatives.

    :param name: Name of the input.
    :param default: Default fallback path.
    :param force_download: Force re-download of file(s) even when they are cached already.
    :return: List of file system paths for all the files for this input.
    """
    if default is None:
        default = []
    input_info = _get_input_info(name, download=DownloadType.ALWAYS if force_download else DownloadType.OPTIONAL)
    if input_info:
        return [file.path for file in input_info.files]
    return default


def get_input_path(name: str, default: Optional[str] = None, force_download: bool = False,) -> Optional[str]:
    """Get path to a file for a given input name.

    Returns a file system path for an input.
    If the input contains multiple files, only the first one is returned.
    If the file(s) are not found in the cache, they are downloaded automatically.

    See get_input_file_paths() or get_input_file_streams() for higher level alternatives.

    :param name: Name of the input.
    :param default: Default fallback path.
    :param force_download: Force re-download of file(s) even when they are cached already.
    :return: File system path to the first file for this input.
    """
    input_paths = get_input_paths(name, force_download=force_download)
    if input_paths:
        return input_paths[0]
    return default


def get_input_file_paths(name: str, force_download: bool = False) -> Iterable[str]:
    """Get paths to all files for a given input name. Auto-extracts compressed archives.

    Returns an Iterable for all file system paths for an input.

    If the file(s) are not found in the cache, they are downloaded automatically.

    If some of the files for the input are compressed/archives, those are automatically
    extracted. In this case, the paths will point to the extracted files and
    not the archive itself.

    See get_input_file_streams() for an alternative.
    See get_input_paths() or get_input_path() for lower level alternatives.

    :param name: Name of the input.
    :param force_download: Force re-download of file(s) even when they are cached already.
    :return: List of file system paths for all the files for this input.
    """
    # TODO: this needs a filter parameter
    # TODO: This name is shitty, c.f. get_input_paths()
    # TODO: How to clean up the VFS's concrete files?
    for file in _get_input_vfs(name, force_download=force_download).files:
        if isinstance(file, vfs.FileInContainer):
            yield file.open_concrete(delete=False).name
        elif isinstance(file, vfs.FileOnDisk):
            yield file.path


def get_input_file_streams(name: str, force_download: bool = False) -> Iterable[IO]:
    """Get file streams to all files for a given input name. Auto-extracts compressed archives.

    Returns an Iterable for file streams for an input.

    If the file(s) are not found in the cache, they are downloaded automatically.

    If some of the files for the input are compressed/archives, those are automatically
    extracted. In this case, the paths in the list will point to the extracted files and
    not the archive itself.

    See get_input_file_paths() for an alternative.
    See get_input_paths() or get_input_path() for lower level alternatives.

    :param name: Name of the input.
    :param force_download: Force re-download of file(s) even when they are cached already.
    :return: List of file system paths for all the files for this input.
    """
    for file in _get_input_vfs(name, force_download=force_download).files:
        yield file.open()


def _uri_to_filename(uri: str) -> str:
    return uri[uri.rfind("/") + 1 :]


def _get_input_vfs(name: str, force_download: bool = False, process_archives: bool = True) -> vfs.VFS:
    v = vfs.VFS()
    ii = _get_input_info(name, download=DownloadType.ALWAYS if force_download else DownloadType.OPTIONAL)
    for file_info in ii.files:
        vfs.add_disk_file(
            v,
            name=file_info.name,
            path=file_info.path,
            process_archives=process_archives,
        )
    return v


def _add_input_info(name: str, info: InputInfo):
    inputs[name] = info


def _get_input_info(name: str, download: Optional[DownloadType] = DownloadType.OPTIONAL) \
        -> Optional[InputInfo]:
    """Get InputInfo for a given input name.

    Looks for the InputInfo from the in-memory cache and if found, downloads the input according
    to the download strategy (Never, Optional, Always)

    If InputInfo not found from in-memory cache, look it up from inputs_config_path and store it.
    If it is found this way, the file is always downloaded already.

    :param name: Name of the input.
    :param download: Download strategy for the input. (Never, Optional, Always)
    :return: InputInfo instance for this input name
    """
    if name in inputs:
        info = inputs[name]
        if download == DownloadType.ALWAYS or not info.is_downloaded() and download == DownloadType.OPTIONAL:
            path = get_inputs_path(name)
            os.makedirs(path, exist_ok=True)
            info.download(get_inputs_path(name), force_download=True if download == DownloadType.ALWAYS else False)
        return info

    inputs_config_path = paths.get_inputs_config_path()
    if os.path.isfile(inputs_config_path):
        with open(inputs_config_path) as json_file:
            data = json.load(json_file)
            input_info_data = data.get(name)
            if input_info_data:
                inputs[name] = InputInfo.from_json_data(input_info_data)
                return inputs[name]
    return None
