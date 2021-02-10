import argparse
import sys

from valohai.config import is_running_in_valohai
from valohai.internals.global_state import input_infos
from valohai.internals.input_info import FileInfo, InputInfo
from valohai.parameters import Parameter


# Step is unused, but it is needed when parsing source code to update valohai.yaml
def prepare(*, step: str, default_parameters: dict = {}, default_inputs: dict = {}):
    """Define the name of the step and it's required inputs and parameters

    Has dual purpose:
    - Provide default values for inputs & parameters so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param default_parameters: Dict of parameters and default values
    :param default_inputs: Dict of inputs with (list of) default URIs

    """
    if not is_running_in_valohai():
        _parse_inputs(default_inputs)
    _parse_parameters(default_parameters)


def _parse_inputs(inputs: dict):
    """Parse inputs into FileInfo objects

    This is only ran for local executions. Cloud execution will parse this same info from inputs.json config.

    :param inputs: Dict with input name as key and default URI as value

    """
    for name, uris in inputs.items():
        if not isinstance(uris, list):
            uris = [uris]
        files = [FileInfo(name=FileInfo.uri_to_filename(uri), uri=uri, path=None, size=None, checksums=None) for uri in uris]
        input_info = InputInfo(files)
        input_infos[name] = input_info


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
        Parameter(name).value = value
    for unknown in unknown_args:
        print(f'Warning: Unexpected command-line argument {unknown} found.', file=sys.stderr)
