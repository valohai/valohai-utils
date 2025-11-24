from typing import Union

from valohai.internals import global_state, global_state_loader

supported_types = Union[int, float, bool, str, None]


def get_parameter_value(name: str, default: supported_types) -> supported_types:
    global_state_loader.load_global_state_if_necessary()
    return global_state.parameters.get(name, default)
