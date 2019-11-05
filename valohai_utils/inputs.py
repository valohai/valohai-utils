import json
import os
from typing import List, Optional

from . import paths
from .internals.input_info import InputInfo


def get_input_info(name) -> Optional[InputInfo]:
    inputs_config_path = paths.get_inputs_config_path()
    if os.path.isfile(inputs_config_path):
        with open(inputs_config_path) as json_file:
            data = json.load(json_file)
        input_info_data = data.get(name)
        if input_info_data:
            return InputInfo.from_json_data(input_info_data)
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
