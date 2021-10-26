from typing import Any, Dict, Optional

from valohai.internals.input_info import InputInfo

loaded: bool = False
inputs: Dict[str, InputInfo] = {}
parameters: Dict[str, Any] = {}
step_name: Optional[str] = None
image_name: Optional[str] = None