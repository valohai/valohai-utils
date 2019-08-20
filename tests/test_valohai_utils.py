import valohai_utils.inputs
import valohai_utils.parameters


def test_get_input_paths(use_test_config_dir):
    assert valohai_utils.inputs.get_input_path("herp") == "/valohai/inputs/herp/Example.jpg"
    assert valohai_utils.inputs.get_input_path("herp", "unused_default") == "/valohai/inputs/herp/Example.jpg"
    assert valohai_utils.inputs.get_input_path("nonono") == ""
    assert valohai_utils.inputs.get_input_path("nonono", "default_path_123") == "default_path_123"


def test_get_parameters(use_test_config_dir):
    assert valohai_utils.parameters.get_parameter("foobar") == 123
    assert valohai_utils.parameters.get_parameter("foobar", 234) == 123
    assert valohai_utils.parameters.get_parameter("test") == "teststr"
    assert valohai_utils.parameters.get_parameter("test", "unused_default") == "teststr"
    assert valohai_utils.parameters.get_parameter("nonono", "hello") == "hello"
    assert not valohai_utils.parameters.get_parameter("nonono")
