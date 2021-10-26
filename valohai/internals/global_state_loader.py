import argparse
import json
import os
import sys
from typing import Dict, Tuple, Set, List, Any, Union

from valohai.internals import global_state
from valohai.internals.input_info import InputInfo
from valohai.paths import get_parameters_config_path, get_inputs_config_path


def load_global_state(
    default_inputs_from_prepare: Dict = None,
    default_parameters_from_prepare: Dict = None
):
    """Loads inputs & parameters and stores their value in the global_state

    Inputs & parameters (with values) can be defined in three places:
    - Call to valohai.prepare()
    - File-based config in inputs.json and parameters.json
    - Overridable values from CLI args

    It is possible that something is defined in all the three places simultaneously.
    Thus, we have a priority order for the final value:

    1. CLI override
    2. File-based config
    3. valohai.prepare()

    :param default_inputs_from_prepare: Dict of inputs and their values from valohai.prepare()
    :param default_parameters_from_prepare: Dict of parameters and their values from valohai.prepare()
    """

    inputs, parameters = {}, {}

    # Load defaults from call to valohai.prepare()
    if default_inputs_from_prepare:
        inputs = sift_defaults(default_inputs_from_prepare)
    if default_parameters_from_prepare:
        parameters = sift_defaults(default_parameters_from_prepare)

    # Use inputs.json and parameters.json instead if found
    file_inputs, file_parameters = load_from_configs()
    inputs = file_inputs or inputs
    parameters = file_parameters or parameters

    # Parse and override input & parameter values from CLI
    cli_inputs, cli_parameters = parse_overrides_from_cli(inputs, parameters)
    inputs = {key: cli_inputs.get(key, value) for key, value in inputs.items()}
    parameters = {key: cli_parameters.get(key, value) for key, value in parameters.items()}

    # Inputs in various formats are converted into InputInfo(s)
    inputs = {key: convert_to_input_info(value) for key, value in inputs.items()}

    # Save results to global_state
    global_state.inputs = inputs
    global_state.parameters = parameters

    # Store an explicit flag to be used in load_global_state_if_necessary()
    global_state.loaded = True


def flush_global_state():
    global_state.loaded = False
    global_state.inputs = {}
    global_state.parameters = {}
    global_state.step_name = None
    global_state.image_name = None


def load_global_state_if_necessary():
    """Loads the global state if it is not already loaded

    It is possible that user hasn't called valohai.prepare() at all,
    but still tries to access inputs and parameters.

    This method is for making sure that the global_state is loaded before accessing them.

    """
    if not global_state.loaded:
        load_global_state()


def parse_overrides_from_cli(inputs: Dict, parameters: Dict) -> Tuple[Dict, Dict]:
    """Override inputs and parameters from the command-line

    :param inputs: Dict of inputs and their values
    :param parameters: Dict of parameters and their values
    """

    parser = argparse.ArgumentParser()
    for name, _ in inputs.items():
        parser.add_argument(f"--{name}", type=str, nargs="+")
    for name, value in parameters.items():
        parser.add_argument(f"--{name}", type=type(value))
    known_args, unknown_args = parser.parse_known_args()

    for unknown in unknown_args:
        print(  # noqa
            f"Warning: Unexpected command-line argument {unknown} found.",
            file=sys.stderr,
        )

    cli_inputs = sift_cli_inputs(known_args, set(inputs.keys()))
    cli_parameters = sift_cli_parameters(known_args, set(parameters.keys()))

    return cli_inputs, cli_parameters



def load_from_configs() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Load input & parameter values from the config file(s)

    Valohai offers mechanism to load inputs & parameters from a JSON config file.
    See if those config files exist and load the values.

    :param default_inputs: Dict of inputs and their default values
    :param default_inputs: Dict of parameters and their default values
    """

    inputs, parameters = {}, {}

    config_path = get_inputs_config_path()
    if os.path.isfile(config_path):
        with open(config_path) as json_file:
            inputs = json.load(json_file)

    config_path = get_parameters_config_path()
    if os.path.isfile(config_path):
        with open(config_path) as json_file:
            parameters = json.load(json_file)

    return inputs, parameters


def sift_cli_inputs(args: argparse.Namespace, expected_keys: Set[str]) -> Dict[str, List[str]]:
    """Sift inputs from all the command-line args

    :param expected_keys: List of expected input names
    """

    result = {}
    for name, values in vars(args).items():
        # Filter out any inputs that we weren't expecting
        if name not in expected_keys:
            continue

        if values is None:
            continue

        if not isinstance(values, list):
            values = [values]

        values = [v for v in values if v is not None]
        if len(values) > 0:
            result[name] = values
    return result


def sift_cli_parameters(args: argparse.Namespace, expected_keys: Set[str]) -> Dict[str, any]:
    """Sift parameters from all the command-line args

    :param expected_keys: List of expected parameter names
    """

    result = {}
    for name, value in vars(args).items():
        # Filter out any parameters that we weren't expecting
        if name not in expected_keys:
            continue

        if value is not None:
            result[name] = value
    return result


def sift_defaults(values: Dict[str, Any]) -> Dict[str, List[str]]:
    """Returns the default values which user defined in .prepare()

    Works for both inputs and parameters.

    We sift from two alternatives (dict and nested dict):

    valohai.prepare(
        default_parameters={"my-param", 123},
        default_inputs={"my-input", "https://lol.png"}
        )
    valohai.prepare(
        default_parameters={"my-param", {"default": 123}},
        default_inputs={"my-input", {"default": "https://lol.png"}}
        )

    :param values: Default values from the .prepare() method
    """

    result = {}
    for key, value in values.items():
        if isinstance(value, dict):
            if "default" in value:
                result[key] = value["default"]
            else:
                raise ValueError(f"No default value defined for {key}")
        else:
            result[key] = value
    return result


def convert_to_input_info(input: Union[str, List[str], Dict]) -> InputInfo:
    """Converts inputs from different formats into an InputInfo

    Inputs can be defined in either .prepare() or inputs.json

    Inputs defined in .prepare() are a List[str] or str
    Inputs defined in inputs.json are a Dict

    Ultimately we want have all of them converted as InputInfo(s)

    :param inputs: Single input as List[str] or Dict
    """
    if isinstance(input, List) or isinstance(input, str):
        return InputInfo.from_urls_and_paths(input)
    return InputInfo.from_json_data(input)
