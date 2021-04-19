import os
from typing import Any, Dict

from valohai_yaml.objs.config import Config
from valohai_yaml.objs.input import Input, KeepDirectories
from valohai_yaml.objs.parameter import Parameter
from valohai_yaml.objs.step import Step

from valohai.consts import DEFAULT_DOCKER_IMAGE
from valohai.internals.parsing import parse

ParameterDict = Dict[str, Any]
InputDict = Dict[str, str]


def generate_step(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict,
) -> Step:
    config_step = Step(
        name=step,
        image=image,
        command=[
            "pip install -r requirements.txt",
            "python %s {parameters}" % relative_source_path,
        ],
    )

    for key, value in parameters.items():
        config_step.parameters[key] = Parameter(
            name=key,
            type=get_parameter_type_name(key, value),
            default=value,
        )

    for key, value in inputs.items():
        has_wildcards = any("*" in uri for uri in value)
        keep_directories = KeepDirectories.SUFFIX.value if has_wildcards else False
        config_step.inputs[key] = Input(
            name=key, default=value, keep_directories=keep_directories
        )
    return config_step


def generate_config(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict,
) -> Config:
    step_obj = generate_step(
        relative_source_path=relative_source_path,
        step=step,
        image=image,
        parameters=parameters,
        inputs=inputs,
    )
    config = Config()
    config.steps[step_obj.name] = step_obj
    return config


def get_source_relative_path(source_path: str, config_path: str) -> str:
    """Return path of a source file relative to config file path

    :param source_path: Path of the Python source code file
    :param config_path: Path of the valohai.yaml config file

    :return: Path of the source code file relative to the config file
    Example:
        config_file_path: /herpderp/valohai.yaml
        source_file_path: /herpderp/somewhere/underneath/test.py
        return: ./somewhere/underneath/test.py
    Ultimately used for creating command with correct relative path in valohai.yaml:
        python ./somewhere/underneath/test.py {parameters}
    """
    relative_source_dir = os.path.relpath(
        os.path.dirname(os.path.abspath(source_path)),
        os.path.dirname(os.path.abspath(config_path)),
    )
    return os.path.join(relative_source_dir, os.path.basename(source_path))


def parse_config_from_source(source_path: str, config_path: str) -> Config:
    with open(source_path) as source_file:
        parsed = parse(source_file.read())
        if not parsed.step:
            raise ValueError("Source is missing a call to valohai.prepare()")
        relative_source_path = get_source_relative_path(source_path, config_path)
        return generate_config(
            relative_source_path=relative_source_path,
            step=parsed.step,
            image=DEFAULT_DOCKER_IMAGE if parsed.image is None else parsed.image,
            parameters=parsed.parameters,
            inputs=parsed.inputs,
        )


def get_parameter_type_name(name: str, value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, float):
        return "float"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, str):
        return "string"

    raise ValueError(
        "Unrecognized parameter type for %s=%s. Supported Python types are float, int, string and bool."
        % (name, value)
    )
