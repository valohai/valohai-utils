import json
import os
from typing import Union, Optional

from . import paths

_parameters = {}
_supported_types = Union[int, float, bool, str]


def add_parameter(name: str, value: _supported_types):
    _parameters[name] = value


def get_parameter(name: str, default: Optional[_supported_types] = None) -> Optional[_supported_types]:
    if name in _parameters:
        return _parameters[name]

    parameters_config_path = paths.get_parameters_config_path()
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                _parameters[name] = data[name]
                return _parameters[name]
    return default
