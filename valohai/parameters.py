import json
import os

from . import paths

_parameters = {}


def add_parameter(name, value):
    _parameters[name] = value


def get_parameter(name, default=None):
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
