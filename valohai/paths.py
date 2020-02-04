import os
from typing import Optional


def get_config_path() -> str:
    return os.environ.get("VH_CONFIG_DIR", "/valohai/config")


def get_inputs_path(input_name: Optional[str] = None) -> str:
    path = os.environ.get("VH_INPUTS_DIR", "/valohai/inputs")
    if input_name:
        path = os.path.join(path, input_name)
    return path


def get_outputs_path(output_name: Optional[str] = None, auto_create: bool = True) -> str:
    path = os.environ.get("VH_OUTPUTS_DIR", "/valohai/outputs")

    # To guard against absolute paths.
    # If the absolute path is in the outputs dir, the path will be made relative.
    # If it is some other absolute path, an exception is raised.
    if os.path.isabs(output_name):
        if output_name.startswith(path):
            output_name = os.path.relpath(output_name, path)
        else:
            raise ValueError("Absolute path used, when relative expected (%s)" % output_name)

    if output_name:
        path = os.path.join(path, output_name)

    if auto_create:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    return path


def get_repository_path() -> str:
    return os.environ.get("VH_REPOSITORY_DIR", "/valohai/repository")


def get_inputs_config_path() -> str:
    return os.path.join(get_config_path(), "inputs.json")


def get_parameters_config_path() -> str:
    return os.path.join(get_config_path(), "parameters.json")
