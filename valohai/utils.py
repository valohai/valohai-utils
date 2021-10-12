import argparse
import sys
from typing import List, Optional

from valohai.internals import global_state


def prepare(
    *,
    step: str,
    default_parameters: Optional[dict] = None,
    default_inputs: Optional[dict] = None,
    image: str = None,
) -> None:
    """Define the name of the step and it's required inputs, parameters and Docker image

    Has dual purpose:
    - Provide default values for inputs, parameters and Docker image so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param default_parameters: Dict of parameters and default values
    :param default_inputs: Dict of inputs with (list of) default URIs
    :param image: Default docker image

    """

    if default_inputs is None:
        default_inputs = {}
    if default_parameters is None:
        default_parameters = {}

    global_state.flush()
    global_state.step_name = step
    global_state.image_name = image
    global_state.default_parameters = default_parameters
    global_state.default_inputs = default_inputs

    parser = argparse.ArgumentParser()
    for name, _ in default_inputs.items():
        parser.add_argument(f"--{name}", type=str, nargs="+")
    for name, value in default_parameters.items():
        parser.add_argument(f"--{name}", type=type(value))
    known_args, unknown_args = parser.parse_known_args()

    _parse_cli_inputs(known_args, list(default_inputs.keys()))
    _parse_cli_parameters(known_args, list(default_parameters.keys()))

    for unknown in unknown_args:
        print(  # noqa
            f"Warning: Unexpected command-line argument {unknown} found.",
            file=sys.stderr,
        )


def _parse_cli_inputs(args: argparse.Namespace, names: List[str]):
    """Pull inputs from the command-line args

    User provides inputs and their default values in a dict, when calling prepare().
    Here we parse possible overrides from the command-line args.

    :param names: List of all possible input names

    """

    for name, values in vars(args).items():
        # Filter out any inputs that we weren't expecting
        if name not in names:
            continue

        if values is None:
            continue

        if not isinstance(values, list):
            values = [values]

        values = [v for v in values if v is not None]
        if len(values) > 0:
            global_state.parsed_cli_inputs[name] = values


def _parse_cli_parameters(args: argparse.Namespace, names: List[str]):
    """Pull parameters from the command-line args

    User provides parameters and their default values in a dict, when calling prepare().
    Here we parse possible overrides from the command-line args.

    :param args: All command-line arguments
    :param names: List of all possible parameters names

    """
    for name, value in vars(args).items():
        # Filter out any parameters that we weren't expecting
        if name not in names:
            continue

        if value is not None:
            global_state.parsed_cli_parameters[name] = value
