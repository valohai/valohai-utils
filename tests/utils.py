import glob
import json
import os


def read_source_files(path_without_ext):
    with open(f"{path_without_ext}.py") as source_python:
        source = source_python.read()
    with open(f"{path_without_ext}.parameters.json") as parameters_json:
        parameters = json.load(parameters_json)
    with open(f"{path_without_ext}.inputs.json") as inputs_json:
        inputs = json.load(inputs_json)
    with open(f"{path_without_ext}.step.json") as step_json:
        step = json.load(step_json)
    return {
        "source": source,
        "parameters": parameters,
        "inputs": inputs,
        "step": step,
    }


def get_parsing_tests():
    basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_parsing")

    for python_file in glob.glob(os.path.join(basepath, "*.py")):
        path_without_ext = os.path.splitext(python_file)[0]
        yield read_source_files(path_without_ext)


def read_yaml_test_data(root_path):
    """
    Returns a list of test sets. Each set is representing a single YAML updating test case.

    Expected in the root_path:
        mytest.py -- Python file defining a step or a pipeline
        mytest.original.valohai.yaml -- Original valohai.yaml
        mytest.expected.valohai.yaml -- Expected valohai.yaml after update
        mytest2.py -- Another Python file defining a step or a pipeline
        mytest2.original.valohai.yaml -- Original valohai.yaml
        mytest2.expected.valohai.yaml -- Expected valohai.yaml after update
        etc...

    """
    test_data = []
    for source_path in glob.glob(f"{root_path}/*.py"):
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
