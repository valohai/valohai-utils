import glob
import json
import os


def read_source_files(path_without_ext):
    with open(f"{path_without_ext}.py", "r") as source_python:
        source = source_python.read()
    with open(f"{path_without_ext}.parameters.json", "r") as parameters_json:
        parameters = json.load(parameters_json)
    with open(f"{path_without_ext}.inputs.json", "r") as inputs_json:
        inputs = json.load(inputs_json)
    with open(f"{path_without_ext}.step.json", "r") as step_json:
        step = json.load(step_json)
    return {
        'source': source,
        'parameters': parameters,
        'inputs': inputs,
        'step': step,
    }


def get_parsing_tests():
    basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_parsing")

    for python_file in glob.glob(os.path.join(basepath, '*.py')):
        path_without_ext = os.path.splitext(python_file)[0]
        yield read_source_files(path_without_ext)
