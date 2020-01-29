import argparse

from valohai.config import is_running_in_valohai
from valohai.inputs import uri_to_filename, add_input_info
from valohai.internals.input_info import FileInfo, InputInfo
from valohai.parameters import add_parameter


def parse_inputs(inputs):
    for name, uris in inputs.items():
        if not isinstance(uris, list):
            uris = [uris]
        files = [FileInfo(name=uri_to_filename(uri), uri=uri) for uri in uris]
        add_input_info(name, InputInfo(files))


def parse_parameters(parameters):
    parser = argparse.ArgumentParser()
    for name, default_value in parameters.items():
        parser.add_argument('--%s' % name, type=type(default_value), default=default_value)
    for name, value in vars(parser.parse_args()).items():
        add_parameter(name, value)


def prepare(*, step, parameters={}, inputs={}):
    if not is_running_in_valohai():
        parse_inputs(inputs)
    parse_parameters(parameters)

