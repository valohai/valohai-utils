import argparse
import glob
import os
import sys
from typing import List

from valohai.config import is_running_in_valohai
from valohai.internals import global_state
from valohai.internals.input_info import FileInfo, InputInfo
from valohai.parameters import Parameter


def prepare(*, step: str, default_parameters: dict = {}, default_inputs: dict = {}):
    """Define the name of the step and it's required inputs and parameters

    Has dual purpose:
    - Provide default values for inputs & parameters so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param default_parameters: Dict of parameters and default values
    :param default_inputs: Dict of inputs with (list of) default URIs

    """
    global_state.step_name = step

    parser = argparse.ArgumentParser()
    for name, default_value in dict(default_inputs).items():
        parser.add_argument('--%s' % name, type=str, nargs='+', default=default_value)
    for name, default_value in dict(default_parameters).items():
        parser.add_argument('--%s' % name, type=type(default_value), default=default_value)
    known_args, unknown_args = parser.parse_known_args()

    if not is_running_in_valohai():
        _load_inputs(known_args, list(default_inputs.keys()))
    _load_parameters(known_args, list(default_parameters.keys()))

    for unknown in unknown_args:
        print(f'Warning: Unexpected command-line argument {unknown} found.', file=sys.stderr)


def _load_inputs(args: argparse.Namespace, names: List[str]):
    """Pull inputs from the command-line args

    User provides inputs and their default values in a dict, when calling prepare().
    Here we parse possible overrides from the command-line args.

    This is only ran for local executions. Cloud execution will get this same info directly from inputs.json.

    :param names: List of all possible input names

    """
    for name, values in vars(args).items():
        if name not in names:
            continue

        if not isinstance(values, list):
            values = [values]

        files = []
        for value in values:
            if "://" not in value:  # The string is a local path
                for path in glob.glob(value):
                    files.append(FileInfo(name=os.path.basename(path), uri=None, path=value, size=None, checksums=None))
            else:  # The string is an URI
                files.append(FileInfo(name=uri_to_filename(value), uri=value, path=None, size=None, checksums=None))

        input_info = InputInfo(files)
        global_state.input_infos[name] = input_info


def _load_parameters(args: argparse.Namespace, names: List[str]):
    """Pull parameters from the command-line args

    User provides parameters and their default values in a dict, when calling prepare().
    Here we parse possible overrides from the command-line args.

    :param args: All command-line arguments
    :param names: List of all possible parameters names

    """
    for name, value in vars(args).items():
        if name not in names:
            continue
        Parameter(name).value = value


def uri_to_filename(uri: str) -> str:
    return uri.rpartition("/")[-1]
