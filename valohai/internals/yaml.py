import copy
import os
from typing import Any, Dict, Optional

import yaml

from valohai.consts import DEFAULT_DOCKER_IMAGE
from valohai.internals.merge import _merge_dicts, _merge_simple
from valohai.internals.parsing import parse
from valohai.paths import get_repository_path
from valohai_yaml import parse as yaml_parse
from valohai_yaml.objs import Config, Parameter, Step
from valohai_yaml.objs.input import Input

ParameterDict = Dict[str, Any]
InputDict = Dict[str, str]


def update_yaml(
    *,
    target_path: str,
    relative_source_path: str,
    step: str,
    parameters: ParameterDict,
    inputs: InputDict
):
    """Updates (or generates) valohai.yaml

    :param target_path: Path to valohai.yaml
    :param relative_source_path: Path to .py file relative to valohai.yaml (used for command)
    :param step: Valohai step name
    :param parameters: Dict of parameter name and default value
    :param inputs: Dict of input name and default URIs

    1. Loads existing Config from valohai.yaml
    2. Updates the Config with the new information
    3. Serializes the updated Config back into valohai.yaml

    """
    new_config = generate_config(
        relative_source_path=relative_source_path,
        step=step,
        image=DEFAULT_DOCKER_IMAGE,
        parameters=parameters,
        inputs=inputs,
    )
    old_config = get_current_config(target_path)
    if old_config:
        new_config = merge_config(old_config, new_config)
    serialize_config_to_yaml(target_path, new_config)


def merge_config(a: Config, b: Config) -> Config:
    result = Config()
    result.steps.update(_merge_dicts(a.steps, b.steps, merge_step))
    return result


def merge_step(a: Step, b: Step) -> Step:
    # If user first types "learning_rage", creates config, and finally fixes the typo,
    # they don't want to end up with both "learning_rage" and "learning_rate" after the merge.
    # So only merge parameters and inputs that are part of both configs (a & b).
    cleaned_parameters_a = {key: a.parameters[key] for key in a.parameters if key in b.parameters.keys()}
    cleaned_inputs_a = {key: a.inputs[key] for key in a.inputs if key in b.inputs.keys()}

    parameters = _merge_dicts(
        cleaned_parameters_a, b.parameters, merger=_merge_simple, copier=copy.deepcopy,
    )
    inputs = _merge_dicts(
        cleaned_inputs_a, b.inputs, merger=_merge_simple, copier=copy.deepcopy,
    )
    # TODO: Logic for merging with existing command
    result = Step(name=b.name, image=b.image, command=b.command)
    result.parameters.update(parameters)
    result.inputs.update(inputs)
    return result


def generate_step(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict
) -> Step:
    config_step = Step(
        name=step, image=image, command="python %s {parameters}" % relative_source_path,
    )

    for key, value in parameters.items():
        config_step.parameters[key] = Parameter(
            name=key, type=get_parameter_type_name(key, value), default=value,
        )

    for key, value in inputs.items():
        config_step.inputs[key] = Input(name=key, default=value,)

    return config_step


def generate_config(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict
) -> Config:
    step = generate_step(
        relative_source_path=relative_source_path,
        step=step,
        image=image,
        parameters=parameters,
        inputs=inputs,
    )
    config = Config()
    config.steps[step.name] = step
    return config


def get_current_config(path: str) -> Optional[Config]:
    if os.path.isfile(path):
        with open(path) as f:
            return yaml_parse(f, validate=True)
    return None


def get_source_relative_path(config_file_path: str, source_file_path: str) -> str:
    """Return path of a source file relative to config file path

    :param config_file_path: Path to the config file (valohai.yaml)
    :param source_file_path: Path to the Python source code file
    :return: Path of the source code file relative to the config file

    Example:
        config_file_path: /herpderp/valohai.yaml
        source_file_path: /herpderp/somewhere/underneath/test.py
        return: ./somewhere/underneath/test.py

    Ultimately used for creating command with correct relative path in valohai.yaml:
        python ./somewhere/underneath/test.py {parameters}

    """
    relative_source_dir = os.path.relpath(
        os.path.dirname(os.path.abspath(source_file_path)),
        os.path.dirname(os.path.abspath(config_file_path)),
    )
    return os.path.join(relative_source_dir, os.path.basename(source_file_path))


def serialize_config_to_yaml(target_path: str, config: Config):
    output = config.serialize()
    with open(target_path, "w") as output_file:
        output_file.write(yaml.safe_dump(output))


def update_yaml_from_source(source_path: str):
    """Updates valohai.yaml by parsing the source code file for a call to valohai.prepare()

    Call to valohai.prepare() will contain step name, parameters and inputs.
    We use the AST parser to parse those from the Python source code file and
    update (or generate) valohai.yaml accordingly.

    :param source_path: Path of the Python source code file

    """
    with open(source_path, "r") as source_file:
        parsed = parse(source_file.read())
        if not parsed.step:
            raise ValueError("Source is missing a call to valohai.prepare()")
        target_path = os.path.join(get_repository_path(), "valohai.yaml")
        relative_source_path = get_source_relative_path(target_path, source_path)
        update_yaml(
            relative_source_path=relative_source_path,
            target_path=target_path,
            step=parsed.step,
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
