from typing import Any, Dict, Optional

from valohai.distributed import Distributed
from valohai.internals.input_info import InputInfo

loaded: bool = False
inputs: Dict[str, InputInfo] = {}
parameters: Dict[str, Any] = {}
step_name: Optional[str] = None
image_name: Optional[str] = None
distributed = Distributed()


def flush_global_state() -> None:
    global loaded, inputs, parameters, step_name, image_name, distributed
    loaded = False
    inputs = {}
    parameters = {}
    step_name = None
    image_name = None
    distributed.flush_state()
