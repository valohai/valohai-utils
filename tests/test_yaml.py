import os
import shutil

import pytest
from valohai_yaml import parse

from tests.utils import compare_yaml, read_yaml_test_data
from valohai.internals.merge import python_to_yaml_merge_strategy
from valohai.internals.yaml import generate_step, parse_config_from_source


@pytest.mark.parametrize(
    "original_yaml, source_python, expected_yaml_filename",
    read_yaml_test_data("tests/test_yaml"),
)
def test_yaml_update_from_source(
    tmpdir, original_yaml, source_python, expected_yaml_filename
):
    yaml_path = os.path.join(tmpdir, "valohai.yaml")
    filename, file_extension = os.path.splitext(source_python)
    source_path = os.path.join(tmpdir, f"test{file_extension}")

    # Build repository with test.py and valohai.yaml
    if os.path.isfile(original_yaml):
        shutil.copy(original_yaml, yaml_path)
    shutil.copy(source_python, source_path)

    # Load original valohai.yaml
    old_config = None
    if os.path.isfile(yaml_path):
        with open(yaml_path) as yaml_file:
            old_config = parse(yaml_file)

    # Parse new config from .py
    new_config = parse_config_from_source(source_path, yaml_path)

    # Merge original and new
    if old_config:
        new_config = old_config.merge_with(new_config, python_to_yaml_merge_strategy)

    # Check against expected result
    with open(expected_yaml_filename) as fp:
        compare_yaml(new_config, fp.read())


def test_posix_path_separator(monkeypatch):
    # Let's be sneaky and force the path separator to simulate Windows
    monkeypatch.setattr(os, "sep", "\\")

    step = generate_step(
        relative_source_path="subfolder\\foo\\bar\\train.py",
        step="train",
        image="python:3.8",
        parameters={},
        inputs={},
    )

    # We expect the path separator be POSIX now
    assert any("subfolder/foo/bar/train.py" in command for command in step.command)
