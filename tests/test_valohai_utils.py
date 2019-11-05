from valohai_utils.parameters import get_parameter


def test_get_parameters(use_test_config_dir):
    assert get_parameter("foobar") == 123
    assert get_parameter("foobar", 234) == 123
    assert get_parameter("test") == "teststr"
    assert get_parameter("test", "unused_default") == "teststr"
    assert get_parameter("nonono", "hello") == "hello"
    assert not get_parameter("nonono")
