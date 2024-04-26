from __future__ import annotations
import dataclasses
import glob
import json
import os

from difflib import unified_diff as diff

from valohai_yaml.objs import Config

from valohai.yaml import config_to_yaml


@dataclasses.dataclass(frozen=True)
class ParsingTestData:
    name: str
    source: str
    parameters: dict
    inputs: dict
    step: dict

    @property
    def image(self) -> str | None:
        return self.step.get("image")

    @property
    def step_name(self) -> str | None:
        return self.step.get("name")


def read_source_files(path_without_ext) -> ParsingTestData:
    with open(f"{path_without_ext}.py") as source_python:
        source = source_python.read()
    with open(f"{path_without_ext}.parameters.json") as parameters_json:
        parameters = json.load(parameters_json)
    with open(f"{path_without_ext}.inputs.json") as inputs_json:
        inputs = json.load(inputs_json)
    with open(f"{path_without_ext}.step.json") as step_json:
        step = json.load(step_json)
    return ParsingTestData(
        name=os.path.basename(path_without_ext),
        source=source,
        parameters=parameters,
        inputs=inputs,
        step=step,
    )


def get_parsing_tests():
    basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_parsing")

    for python_file in glob.glob(os.path.join(basepath, "*.py")):
        path_without_ext = os.path.splitext(python_file)[0]
        yield read_source_files(path_without_ext)


def read_yaml_test_data(root_path):
    """
    Returns a list of test sets. Each set is representing a single YAML updating test case.

    Expected in the root_path:
        mytest.py -- Python (or .ipynb) file defining a step or a pipeline
        mytest.original.valohai.yaml -- Original valohai.yaml
        mytest.expected.valohai.yaml -- Expected valohai.yaml after update
        mytest2.py -- Another Python file defining a step or a pipeline
        mytest2.original.valohai.yaml -- Original valohai.yaml
        mytest2.expected.valohai.yaml -- Expected valohai.yaml after update
        etc...

    """
    test_data = []
    for source_path in glob.glob(f"{root_path}/*.py") + glob.glob(
        f"{root_path}/*.ipynb"
    ):
        dirname = os.path.dirname(source_path)
        name, extension = os.path.splitext(os.path.basename(source_path))
        test_data.append(
            (
                f"{dirname}/{name}.original.valohai.yaml",
                source_path,
                f"{dirname}/{name}.expected.valohai.yaml",
            )
        )
    return test_data


def compare_yaml(config: Config, fixture_yaml: str) -> None:
    generated_yaml = config_to_yaml(config)
    assert generated_yaml == fixture_yaml, "\n".join(
        diff(
            generated_yaml.splitlines(),
            fixture_yaml.splitlines(),
        )
    )
