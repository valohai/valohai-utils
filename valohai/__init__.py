__version__ = "0.1.11"

import papi

from .inputs import inputs
from .metadata import logger
from .outputs import outputs
from .parameters import parameters
from .prepare_impl import prepare

Pipeline = papi.Papi

__all__ = ["inputs", "logger", "outputs", "parameters", "prepare", "Pipeline"]
