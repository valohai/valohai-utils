from valohai.internals.parameters import get_parameter_value, supported_types


class Parameter:
    def __init__(self, name: str, default: supported_types = None) -> None:
        self.name = str(name)
        self.default = default

    @property
    def value(self) -> supported_types:
        result = get_parameter_value(self.name, self.default)
        return result


parameters = Parameter
