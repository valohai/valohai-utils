import json
import os

import valohai_utils.paths as config


def get_parameter(name, default=None):
    parameters_config_path = config.get_parameters_config_path()
    if os.path.isfile(parameters_config_path):
        with open(parameters_config_path) as json_file:
            data = json.load(json_file)
            if name in data:
                return data[name]
    return default
