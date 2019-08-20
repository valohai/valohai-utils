import os
import json

# config_path = '/valohai/config/inputs.json'
inputs_config_path = "./tests/config/inputs.json"


def get_input_path(name, default=""):
    files = get_input_paths(name)
    if len(files) > 0:
        return files[0]
    return default


def get_input_paths(name, default=[]):
    if os.path.isfile(inputs_config_path):
        with open(inputs_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                if len(data[name]['files']) > 0:
                    result = []
                    for file in data[name]['files']:
                        result.append(file['path'])
                    return result
    return default
