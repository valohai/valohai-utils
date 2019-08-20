import os
import json

# config_path = '/valohai/config/inputs.json'
parameters_config_path = "./tests/config/parameters.json"


def get_parameter(name, default=None):
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                return data[name]
    return default
