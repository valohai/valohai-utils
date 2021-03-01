import glob
import os
import shutil

import pytest
from valohai_yaml import parse

from valohai.internals.merge import python_to_yaml_merge_strategy
from valohai.internals.yaml import parse_config_from_source
from valohai.yaml import config_to_yaml


def read_test_data():
    """
    Expected files (tests/test_yaml):
        mytest.py -- Python file calling valohai.prepare()
        mytest.original.valohai.yaml -- Original valohai.yaml
        mytest.expected.valohai.yaml -- Expected valohai.yaml after update
    """
    test_data = []
    for source_path in glob.glob("tests/test_yaml/*.py"):
        dirname = os.path.dirname(source_path)
        name, extension = os.path.splitext(os.path.basename(source_path))
        test_data.append(
            (
                "%s/%s.original.valohai.yaml" % (dirname, name),
                source_path,
                "%s/%s.expected.valohai.yaml" % (dirname, name),
            )
        )
    return test_data


@pytest.mark.parametrize(
    "original_yaml, source_python, expected_yaml", read_test_data()
)
def test_yaml_update_from_source(tmpdir, original_yaml, source_python, expected_yaml):
    yaml_path = os.path.join(tmpdir, "valohai.yaml")
    source_path = os.path.join(tmpdir, "test.py")

    # Build repository with test.py and valohai.yaml
    if os.path.isfile(original_yaml):
        shutil.copy(original_yaml, yaml_path)
    shutil.copy(source_python, source_path)

    # Load original valohai.yaml
    old_config = None
    if os.path.isfile(yaml_path):
        with open(yaml_path, "r") as yaml_file:
            old_config = parse(yaml_file)

    # Parse new config from .py
    new_config = parse_config_from_source(source_path, yaml_path)

    # Merge original and new
    if old_config:
        new_config = old_config.merge_with(new_config, python_to_yaml_merge_strategy)

    # Check against expected result
    with open(expected_yaml, "r") as expected_yaml:
        new_yaml = config_to_yaml(new_config)
        assert new_yaml == expected_yaml.read()
