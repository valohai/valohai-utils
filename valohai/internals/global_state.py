from typing import Any, Dict, Optional

inputs_cache: Dict[str, Any] = {}
parameters_cache: Dict[str, Any] = {}
parsed_cli_inputs: Dict[str, Any] = {}
parsed_cli_parameters: Dict[str, Any] = {}
default_inputs: Dict[str, Any] = {}
default_parameters: Dict[str, Any] = {}
step_name = ""
image_name: Optional[str] = ""


def flush():
    global inputs_cache, parameters_cache, parsed_cli_inputs, parsed_cli_parameters, default_inputs, default_parameters, step_name, image_name
    inputs_cache = {}
    parameters_cache = {}
    parsed_cli_inputs = {}
    parsed_cli_parameters = {}
    default_inputs = {}
    default_parameters = {}
    step_name = ""
    image_name = ""
