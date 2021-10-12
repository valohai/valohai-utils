from typing import Any, Union


def sift_default_value(name: str, value: Union[float, int, str, bool, dict]) -> Any:
    """
    Returns the default value which user defined in .prepare(). Works for both inputs and parameters.

    We support two alternatives (dict and nested dict):

    valohai.prepare(
        default_parameters={"my-param", 123},
        default_inputs={"my-input", "https://lol.png"}
        )
    valohai.prepare(
        default_parameters={"my-param", {"default": 123}},
        default_inputs={"my-input", {"default": "https://lol.png"}}
        )

    """
    if isinstance(value, dict):
        if "default" in value:
            return value["default"]
        else:
            raise ValueError(f"No default value defined for {name}")
    return value


def uri_to_filename(uri: str) -> str:
    return uri.rpartition("/")[-1]
