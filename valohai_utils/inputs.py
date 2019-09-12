import json
import os

from . import paths


def get_input_path(name, default=""):
    return get_input_paths(name, [default])[0]


def get_input_paths(name, default=None):
    if default is None:
        default = []
    inputs_config_path = paths.get_inputs_config_path()
    if os.path.isfile(inputs_config_path):
        with open(inputs_config_path) as json_file:
            data = json.load(json_file)
        input_info = data.get(name)
        if input_info:
            files = input_info.get('files', ())
            if files:
                return [file['path'] for file in files]
    return default
