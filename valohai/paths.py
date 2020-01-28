import os
import uuid

from valohai.config import is_running_in_valohai
from valohai.consts import VH_LOCAL_CONFIG_DIR, VH_LOCAL_INPUTS_DIR, VH_LOCAL_OUTPUTS_DIR

execution_guid = None


def get_config_path():
    return os.environ.get("VH_CONFIG_DIR", "/valohai/config" if is_running_in_valohai() else VH_LOCAL_CONFIG_DIR)


def get_inputs_path(input_name=None):
    path = os.environ.get("VH_INPUTS_DIR", "/valohai/inputs" if is_running_in_valohai() else VH_LOCAL_INPUTS_DIR)
    if input_name:
        path = os.path.join(path, input_name)
    return path


def get_outputs_path():
    if is_running_in_valohai():
        return os.environ.get("VH_OUTPUTS_DIR", "/valohai/outputs")
    else:
        return os.path.join(VH_LOCAL_OUTPUTS_DIR, get_execution_guid())


def get_repository_path():
    return os.environ.get("VH_REPOSITORY_DIR", "/valohai/repository" if is_running_in_valohai() else ".")


def get_inputs_config_path():
    return os.path.join(get_config_path(), "inputs.json")


def get_parameters_config_path():
    return os.path.join(get_config_path(), "parameters.json")


def get_execution_guid():
    global execution_guid
    if not execution_guid:
        execution_guid = uuid.uuid4().hex
    return execution_guid
