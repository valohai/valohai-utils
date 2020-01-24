import glob
import os
import pytest
import json
from .valohai_test_environment import ValohaiTestEnvironment


@pytest.fixture
def vte(tmpdir):
    return ValohaiTestEnvironment(root_dir=str(tmpdir.mkdir("valohai")))


@pytest.fixture
def source_codes():
    result = []
    basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_parsing")

    for python_file in glob.glob(os.path.join(basepath, '*.py')):
        path_without_ext = os.path.splitext(python_file)[0]
        with open("%s.py" % path_without_ext, "r") as source_python, \
            open("%s.parameters.json" % path_without_ext, "r") as parameters_json, \
            open("%s.inputs.json" % path_without_ext, "r") as inputs_json, \
            open("%s.step.json" % path_without_ext, "r") as step_json:
            result.append({
                'source': source_python.read(),
                'parameters': json.loads(parameters_json.read()),
                'inputs': json.loads(inputs_json.read()),
                'step': json.loads(step_json.read())
            })
    return result


@pytest.fixture
def use_test_config_dir(vte, monkeypatch):
    vte.build()
    monkeypatch.setenv("VH_CONFIG_DIR", str(vte.config_path))
    monkeypatch.setenv("VH_INPUT_DIR", str(vte.inputs_path))
    monkeypatch.setenv("VH_OUTPUT_DIR", str(vte.outputs_path))
