from valohai.internals.parameters import get_parameter_value, supported_types


class Parameter:
    def __init__(self, name: str, default: supported_types = None) -> None:
        self.name = str(name)
        self.default = default

    @property
    def value(self) -> supported_types:
        return get_parameter_value(self.name, self.default)


parameters = Parameter
