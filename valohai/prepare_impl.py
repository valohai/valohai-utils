from typing import Optional

from valohai.internals import global_state
from valohai.internals.global_state_loader import load_global_state
from valohai.types import InputDict, ParameterDict


def prepare(
    *,
    step: str,
    default_parameters: Optional[ParameterDict] = None,
    default_inputs: Optional[InputDict] = None,
    image: Optional[str] = None,
) -> None:
    """Define the name of the step and it's required inputs, parameters and Docker image

    Has dual purpose:
    - Provide default values for inputs, parameters and Docker image so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param default_parameters: Dict of parameters and default values
    :param default_inputs: Dict of inputs with (list of) default URIs
    :param image: Default docker image

    """

    global_state.step_name = step
    global_state.image_name = image

    load_global_state(
        default_inputs_from_prepare=default_inputs,
        default_parameters_from_prepare=default_parameters,
    )
