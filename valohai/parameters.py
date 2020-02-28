import json
import os
from typing import Optional, Union

from valohai.internals.global_state import parameters

from . import paths

_supported_types = Union[int, float, bool, str]


def add_parameter(name: str, value: _supported_types):
    parameters[name] = value


def get_parameter(name: str, default: Optional[_supported_types] = None) -> Optional[_supported_types]:
    if name in parameters:
        return parameters[name]

    parameters_config_path = paths.get_parameters_config_path()
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                parameters[name] = data[name]
                return parameters[name]
    return default
