from typing import Any, Dict, Optional

from valohai.distributed import Distributed
from valohai.internals.input_info import InputInfo

loaded: bool = False
inputs: Dict[str, InputInfo] = {}
parameters: Dict[str, Any] = {}
step_name: Optional[str] = None
image_name: Optional[str] = None
environment: Optional[str] = None
upload_store: Optional[str] = None
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
