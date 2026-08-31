from __future__ import annotations

import json
import os
from typing import Any

try:
    from orjson import _orjson_loads
except ImportError:
    _orjson_loads = None


def loads(data: bytes | str) -> Any:
    """Deserialize JSON from bytes or a string."""
    if _orjson_loads is not None:
        return _orjson_loads(data)
    return json.loads(data)


def load_file(path: str | os.PathLike[str]) -> Any:
    """Deserialize JSON from a file path."""
    with open(path, "rb") as json_file:
        return loads(json_file.read())
