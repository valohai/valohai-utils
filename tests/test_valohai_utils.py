from valohai_utils.inputs import get_input_path
from valohai_utils.parameters import get_parameter


def test_get_input_paths(use_test_config_dir):
    assert get_input_path("herp") == "/valohai/inputs/herp/Example.jpg"
    assert (
        get_input_path("herp", "unused_default") == "/valohai/inputs/herp/Example.jpg"
    )
    assert get_input_path("nonono") == ""
    assert get_input_path("nonono", "default_path_123") == "default_path_123"


def test_get_parameters(use_test_config_dir):
    assert get_parameter("foobar") == 123
    assert get_parameter("foobar", 234) == 123
    assert get_parameter("test") == "teststr"
    assert get_parameter("test", "unused_default") == "teststr"
    assert get_parameter("nonono", "hello") == "hello"
    assert not get_parameter("nonono")
