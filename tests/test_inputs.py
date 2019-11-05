from valohai_utils.inputs import get_input_path


def test_get_input_paths(use_test_config_dir):
    assert get_input_path("single_image").endswith(
        "/valohai/inputs/single_image/Example.jpg"
    )
    assert get_input_path("single_image", "unused_default").endswith(
        "/valohai/inputs/single_image/Example.jpg"
    )
    assert get_input_path("nonono") == ""
    assert get_input_path("nonono", "default_path_123") == "default_path_123"
