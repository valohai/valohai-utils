import json
import os

from . import paths


def get_parameter(name, default=None):
    parameters_config_path = paths.get_parameters_config_path()
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                return data[name]
    return default
