import os
import shutil

import pytest
from valohai_yaml import parse

from tests.utils import compare_yaml, read_yaml_test_data
from valohai.internals.pipeline import get_pipeline_from_source


@pytest.mark.parametrize(
    "original_yaml, source_python, expected_yaml_filename",
    read_yaml_test_data("tests/test_pipeline_yaml"),
)
def test_pipeline_yaml_update_from_source(
    tmpdir, original_yaml, source_python, expected_yaml_filename
):
    yaml_path = os.path.join(tmpdir, "valohai.yaml")
    source_path = os.path.join(tmpdir, "test.py")

    # Build repository with test.py and valohai.yaml
    if os.path.isfile(original_yaml):
        shutil.copy(original_yaml, yaml_path)
    shutil.copy(source_python, source_path)

    # Load original valohai.yaml
    with open(yaml_path) as yaml_file:
        old_config = parse(yaml_file)

    # Parse new config from .py
    new_config = get_pipeline_from_source(source_path, old_config)

    # Merge original and new
    new_config = old_config.merge_with(new_config)

    # Check against expected result
    with open(expected_yaml_filename) as fp:
        compare_yaml(new_config, fp.read())
