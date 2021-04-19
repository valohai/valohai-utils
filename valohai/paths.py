import os
from typing import Optional

from valohai.config import is_running_in_valohai
from valohai.consts import (
    VH_LOCAL_CONFIG_DIR,
    VH_LOCAL_INPUTS_DIR,
    VH_LOCAL_OUTPUTS_DIR,
    VH_LOCAL_REPOSITORY_DIR,
)
from valohai.internals import global_state
from valohai.internals.guid import get_execution_guid


def get_config_path() -> str:
    return os.environ.get(
        "VH_CONFIG_DIR",
        "/valohai/config" if is_running_in_valohai() else VH_LOCAL_CONFIG_DIR,
    )


def get_inputs_path(input_name: Optional[str] = None) -> str:
    if is_running_in_valohai():
        path = os.environ.get("VH_INPUTS_DIR", "/valohai/inputs")
    else:
        path = os.environ.get(
            "VH_INPUTS_DIR", os.path.join(VH_LOCAL_INPUTS_DIR, global_state.step_name)
        )

    if input_name:
        return os.path.join(path, input_name)
    return path


def get_outputs_path() -> str:
    if is_running_in_valohai():
        return os.environ.get("VH_OUTPUTS_DIR", "/valohai/outputs")
    else:
        return os.environ.get(
            "VH_OUTPUTS_DIR",
            os.path.join(
                VH_LOCAL_OUTPUTS_DIR, get_execution_guid(), global_state.step_name
            ),
        )


def get_repository_path() -> str:
    return os.environ.get(
        "VH_REPOSITORY_DIR",
        "/valohai/repository" if is_running_in_valohai() else VH_LOCAL_REPOSITORY_DIR,
    )


def get_inputs_config_path() -> str:
    return os.path.join(get_config_path(), "inputs.json")


def get_parameters_config_path() -> str:
    return os.path.join(get_config_path(), "parameters.json")
