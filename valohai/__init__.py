__version__ = "0.1.6"

import papi

from .inputs import inputs
from .metadata import logger
from .outputs import outputs
from .parameters import parameters
from .utils import prepare

Pipeline = papi.Papi

__all__ = ["inputs", "logger", "outputs", "parameters", "prepare", "Pipeline"]
