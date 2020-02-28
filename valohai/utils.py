import argparse
import sys

from valohai.config import is_running_in_valohai
from valohai.inputs import _uri_to_filename, _add_input_info
from valohai.internals.input_info import FileInfo, InputInfo
from valohai.parameters import add_parameter


# Step is unused, but it is needed when parsing source code to update valohai.yaml
def prepare(*, step: str, parameters: dict = {}, inputs: dict = {}):
    """Define the name of the step and it's required inputs and parameters

    Has dual purpose:
    - Provide default values for inputs & parameters so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param parameters: Dict of parameters and default values
    :param inputs: Dict of inputs with (list of) default URIs

    """
    if not is_running_in_valohai():
        _parse_inputs(inputs)
    _parse_parameters(parameters)


def _parse_inputs(inputs: dict):
    """Parse inputs into FileInfo objects

    This is only ran for local executions. Cloud execution will parse this same info from inputs.json config.

    :param inputs: Dict with input name as key and default URI as value

    """
    for name, uris in inputs.items():
        if not isinstance(uris, list):
            uris = [uris]
        files = [FileInfo(name=_uri_to_filename(uri), uri=uri, path=None, size=None, checksums=None) for uri in uris]
        _add_input_info(name, InputInfo(files))


def _parse_parameters(parameters: dict):
    """Parse parameters from command-line or use the defaults from the dict

    User provides parameters and their default values in a dict, when calling prepare().
    Here we parse all possible overrides from command-line and store the final value.
    Parameter type is deducted from the default value.

    :param parameters: Dict with parameter name as key and default value

    """
    parser = argparse.ArgumentParser()
    for name, default_value in parameters.items():
        parser.add_argument('--%s' % name, type=type(default_value), default=default_value)
    known_args, unknown_args = parser.parse_known_args()
    for name, value in vars(known_args).items():
        add_parameter(name, value)
    for unknown in unknown_args:
        print(f'Warning: Unexpected command-line argument {unknown} found.', file=sys.stderr)
