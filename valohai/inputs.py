import json
import os
from typing import IO, Iterable, List, Optional

from . import paths
from .internals import vfs
from .internals.input_info import InputInfo

_inputs = {}


def uri_to_filename(uri):
    return uri[uri.rfind("/") + 1:]


def add_input_info(name, info):
    _inputs[name] = info


def get_input_info(name) -> Optional[InputInfo]:
    if name in _inputs:
        return _inputs[name]

    inputs_config_path = paths.get_inputs_config_path()
    if os.path.isfile(inputs_config_path):
        with open(inputs_config_path) as json_file:
            data = json.load(json_file)
            input_info_data = data.get(name)
            if input_info_data:
                _inputs[name] = InputInfo.from_json_data(input_info_data)
                return _inputs[name]
    return None


def get_input_paths(name, default=None) -> List[str]:
    if default is None:
        default = []
    input_info = get_input_info(name)
    if input_info:
        return [file.path for file in input_info.files]
    return default


def get_input_path(name, default="") -> str:
    return get_input_paths(name, [default])[0]


def get_input_vfs(name, process_archives: bool = True) -> vfs.VFS:
    v = vfs.VFS()
    ii = get_input_info(name)
    for file_info in ii.files:
        vfs.add_disk_file(
            v,
            name=file_info.name,
            path=file_info.path,
            process_archives=process_archives,
        )
    return v


def get_input_file_paths(name) -> Iterable[str]:
    # TODO: this needs a filter parameter
    # TODO: This name is shitty, c.f. get_input_paths()
    # TODO: How to clean up the VFS's concrete files?
    for file in get_input_vfs(name):
        if isinstance(file, vfs.FileInContainer):
            yield file.open_concrete(delete=False).name
        elif isinstance(file, vfs.FileOnDisk):
            yield file.path


def get_input_file_streams(name) -> Iterable[IO]:
    for file in get_input_vfs(name):
        yield file.open()
