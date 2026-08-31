__version__ = "0.8.0"

import papi

from valohai.controller_api import set_status_detail
from valohai.execution import execution
from valohai.inputs import inputs
from valohai.internals.global_state import distributed
from valohai.metadata import logger
from valohai.output_properties import output_properties
from valohai.outputs import outputs
from valohai.parameters import parameters
from valohai.prepare_impl import prepare
from valohai.triggers import triggers

Pipeline = papi.Papi

__all__ = [
    "Pipeline",
    "distributed",
    "execution",
    "inputs",
    "logger",
    "output_properties",
    "outputs",
    "parameters",
    "prepare",
    "set_status_detail",
    "triggers",
]
