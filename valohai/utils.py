import json
import os

from valohai.internals.input_info import InputInfo, FileInfo

from valohai.config import is_running_in_valohai
from valohai.paths import get_parameters_config_path, get_inputs_config_path, get_config_path


def prepare(*, step, parameters={}, inputs={}):
    if not is_running_in_valohai():
        config_path = get_config_path()
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        with open(get_parameters_config_path(), "w") as params_file:
            params_file.write(get_parameters_config_json(parameters))
        with open(get_inputs_config_path(), "w") as inputs_file:
            inputs_file.write(get_inputs_config_json(inputs))


def get_parameters_config_json(parameters):
    return json.dumps(parameters)


def get_inputs_config_json(inputs):
    result = {}

    for name, uris in inputs.items():
        if not isinstance(uris, list):
            uris = [uris]
        files = [FileInfo(uri=uri) for uri in uris]
        result.update(InputInfo(name=name, files=files).serialize())

    return json.dumps(result)
