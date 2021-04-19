from valohai.internals import global_state
from valohai.internals.parameters import load_parameter, supported_types


class Parameter:
    def __init__(self, name: str, default: supported_types = None) -> None:
        self.name = str(name)
        self.default = default

    @property
    def value(self) -> supported_types:
        if self.name in global_state.parsed_parameters:
            return global_state.parsed_parameters[self.name]
        return load_parameter(self.name, self.default)

    @value.setter
    def value(self, value: supported_types):
        global_state.parsed_parameters[self.name] = value


parameters = Parameter
