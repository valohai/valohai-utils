from __future__ import annotations

from typing import Any

from valohai.distributed import Distributed
from valohai.internals.input_info import InputInfo

loaded: bool = False
inputs: dict[str, InputInfo] = {}
parameters: dict[str, Any] = {}
step_name: str | None = None
image_name: str | None = None
environment: str | None = None
upload_store: str | None = None
distributed = Distributed()
multifile: bool = False


def flush_global_state() -> None:
    # fmt: off
    global loaded, inputs, parameters, step_name, image_name, distributed, environment, upload_store, multifile
    # fmt: off
    loaded = False
    inputs = {}
    parameters = {}
    step_name = None
    image_name = None
    environment = None
    upload_store = None
    multifile = False
    distributed.flush_state()
