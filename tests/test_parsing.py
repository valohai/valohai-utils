import pytest

from valohai.internals.parsing import parse

from .utils import get_parsing_tests


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
        )


@pytest.mark.parametrize("source, parameters, inputs, step", read_test_data())
def test_parse(source, inputs, parameters, step):
    result = parse(source)

    assert result.inputs == inputs
    assert result.parameters == parameters
    assert result.step == step
