import valohai


def test_get_parameters(use_test_config_dir):
    assert valohai.parameters("foobar").value == 123
    assert valohai.parameters("foobar", 234).value == 123
    assert valohai.parameters("test").value == "teststr"
    assert valohai.parameters("test", "unused_default").value == "teststr"
    assert valohai.parameters("missing_parameter", "hello").value == "hello"
    assert not valohai.parameters("nonono").value
