from valohai.internals.global_state import parsed_parameters
from .internals.parameters import load_parameter, supported_types


class Parameter:
    def __init__(self, name: str, default: supported_types = None):
        self.name = str(name)
        self.default = default

    @property
    def value(self) -> supported_types:
        if self.name in parsed_parameters:
            return parsed_parameters[self.name]
        return load_parameter(self.name, self.default)

    @value.setter
    def value(self, value: supported_types):
        parsed_parameters[self.name] = value


parameters = Parameter
