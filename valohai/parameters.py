import json
import os
from typing import Optional, Union

from valohai.internals.global_state import parsed_parameters

from . import paths

_supported_types = Union[int, float, bool, str, None]


def parameters(name: str, default: _supported_types = None):
    return Parameter(name, default)


class Parameter:
    def __init__(self, name: str, default: _supported_types = None):
        self.name = name
        self.default = default

    @property
    def value(self) -> _supported_types:
        if self.name in parsed_parameters:
            return parsed_parameters[self.name]

        parameters_config_path = paths.get_parameters_config_path()
        if os.path.isfile(parameters_config_path):
            with open(parameters_config_path) as json_file:
                data = json.load(json_file)
                if self.name in data:
                    parsed_parameters[self.name] = data[self.name]
                    return parsed_parameters[self.name]
        return self.default

    @value.setter
    def value(self, value: _supported_types):
        parsed_parameters[self.name] = value
