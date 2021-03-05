import pytest

from valohai.internals.parsing import parse

from .utils import get_parsing_tests
from valohai.consts import DEFAULT_DOCKER_IMAGE


def read_test_data():
    """
    Expected files (tests/test_parsing):
        mytest.py -- Python file calling valohai.prepare()
        mytest.inputs.json -- Expected parsed inputs
        mytest.parameters.json -- Expected parsed parameters
        mytest.step.json -- Expected parsed step
    """
    for info in get_parsing_tests():
        yield (
            info["source"],
            info["parameters"],
            info["inputs"],
            info["step"]["name"],
            info["step"]["image"] if 'image' in info["step"] else DEFAULT_DOCKER_IMAGE,
        )


@pytest.mark.parametrize("source, parameters, inputs, step, image", read_test_data())
def test_parse(source, inputs, parameters, step, image):
    result = parse(source)

    assert result.inputs == inputs
    assert result.parameters == parameters
    assert result.step == step
    assert result.image == image