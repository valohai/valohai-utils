import json
import os
from typing import Optional, Union

from valohai.internals import global_state
from valohai.internals.utils import sift_default_value
from valohai.paths import get_parameters_config_path

supported_types = Union[int, float, bool, str, None]


def get_parameter_value(name: str, default: supported_types) -> supported_types:
    if name in global_state.parameters_cache:
        return global_state.parameters_cache[name]

    result = find_parameter_value(name) or default

    if result:
        global_state.parameters_cache[name] = result

    return result


def find_parameter_value(name: str) -> Optional[supported_types]:
    """Find the value for a given parameter name.

    The value can be from various sources (in the order of priority):
    1. Command-line argument
    2. parameters.json Valohai config
    3. default_parameters from valohai.prepare()

    :param name: Name of the parameter.
    :return: Value of the parameter
    """

    # Option 1: Command-line argument
    if name in global_state.parsed_cli_parameters:
        return global_state.parsed_cli_parameters[name]

    # Option 2: parameters.json Valohai config
    if os.path.isfile(get_parameters_config_path()):
        with open(get_parameters_config_path()) as json_file:
            data = json.load(json_file)
            if name in data:
                return data[name]

    # Option 3: default_parameters from valohai.prepare()
    if name in global_state.default_parameters:
        return sift_default_value(name, global_state.default_parameters[name])

    return None
