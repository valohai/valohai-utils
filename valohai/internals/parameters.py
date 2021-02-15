import json
import os
from typing import Union

from valohai.internals import global_state
from valohai.paths import get_parameters_config_path

supported_types = Union[int, float, bool, str, None]


def load_parameter(name: str, default: supported_types) -> supported_types:
    parameters_config_path = get_parameters_config_path()
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                global_state.parsed_parameters[name] = data[name]
                return global_state.parsed_parameters[name]
    return default
