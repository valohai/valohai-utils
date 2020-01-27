import os

from valohai.config import is_running_in_valohai


def get_config_path():
    return os.environ.get("VH_CONFIG_DIR", "/valohai/config" if is_running_in_valohai() else ".valohai/config")


def get_inputs_path(input_name=None):
    path = os.environ.get("VH_INPUTS_DIR", "/valohai/inputs" if is_running_in_valohai() else ".valohai/inputs")
    if input_name:
        path = os.path.join(path, input_name)
    return path


def get_outputs_path():
    return os.environ.get("VH_INPUTS_DIR", "/valohai/outputs" if is_running_in_valohai() else ".valohai/outputs")


def get_repository_path():
    return os.environ.get("VH_REPOSITORY_DIR", "/valohai/outputs" if is_running_in_valohai() else ".")


def get_inputs_config_path():
    return os.path.join(get_config_path(), "inputs.json")


def get_parameters_config_path():
    return os.path.join(get_config_path(), "parameters.json")
