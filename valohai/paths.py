import os


def get_config_path():
    return os.environ.get("VH_CONFIG_DIR", "/valohai/config")


def get_inputs_path(input_name=None):
    path = os.environ.get("VH_INPUTS_DIR", "/valohai/inputs")
    if input_name:
        path = os.path.join(path, input_name)
    return path


def get_outputs_path():
    return os.environ.get("VH_INPUTS_DIR", "/valohai/outputs")


def get_repository_path():
    return os.environ.get("VH_REPOSITORY_DIR", "/valohai/repository")


def get_inputs_config_path():
    return os.path.join(get_config_path(), "inputs.json")


def get_parameters_config_path():
    return os.path.join(get_config_path(), "parameters.json")
