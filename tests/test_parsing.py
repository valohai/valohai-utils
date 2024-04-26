import pytest

from valohai.internals.parsing import parse
from .utils import get_parsing_tests, ParsingTestData


@pytest.mark.parametrize("test_data", get_parsing_tests(), ids=lambda ptd: ptd.name)
def test_parse(test_data: ParsingTestData):
    """
    Expected files (tests/test_parsing):
        mytest.py -- Python (or .ipynb) file calling valohai.prepare()
        mytest.inputs.json -- Expected parsed inputs
        mytest.parameters.json -- Expected parsed parameters
        mytest.step.json -- Expected parsed step
    """
    result = parse(test_data.source)

    assert result.inputs == test_data.inputs
    assert result.parameters == test_data.parameters
    assert result.step == test_data.step_name
    assert result.image == test_data.image
