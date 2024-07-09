__version__ = "0.5.0"

import papi

from valohai.controller_api import set_status_detail
from valohai.inputs import inputs
from valohai.internals.global_state import distributed
from valohai.metadata import logger
from valohai.outputs import outputs
from valohai.parameters import parameters
from valohai.prepare_impl import prepare
from valohai.triggers import triggers

Pipeline = papi.Papi

__all__ = [
    "distributed",
    "inputs",
    "logger",
    "outputs",
    "parameters",
    "prepare",
    "Pipeline",
    "set_status_detail",
    "triggers",
]
