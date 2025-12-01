from typing import Any, Dict, List, Union, Protocol

InputDict = Dict[str, Union[str, List[str], Dict[str, Any]]]
ParameterDict = Dict[str, Union[int, bool, float, str, Dict[str, Any]]]


class CanWriteBytes(Protocol):
    """Type checking protocol for objects that can write bytes."""

    def write(self, data: bytes) -> int: ...
