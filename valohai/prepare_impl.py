from __future__ import annotations

from valohai.internals import global_state
from valohai.internals.global_state_loader import load_global_state
from valohai.types import InputDict, ParameterDict


def prepare(
    *,
    step: str,
    default_parameters: ParameterDict | None = None,
    default_inputs: InputDict | None = None,
    image: str | None = None,
    environment: str | None = None,
    multifile: bool = False,
    upload_store: str | None = None,
) -> None:
    """Define the name of the step and its required inputs, parameters and Docker image

    Has dual purpose:
    - Provide default values for inputs, parameters and Docker image so the user code can be executed
    - Provide entry-point for the parser that generates/updates valohai.yaml integration file

    :param step: Step name for valohai.yaml
    :param default_parameters: Dict of parameters and default values
    :param default_inputs: Dict of inputs with (list of) default URIs
    :param image: Default docker image
    :param environment: Default environment ID or slug
    :param multifile: allow step to be prepared from multiple different source files
    :param upload_store: Upload store UUID for storing execution outputs
    """

    global_state.step_name = step
    global_state.image_name = image
    global_state.environment = environment
    global_state.multifile = multifile
    global_state.upload_store = upload_store

    load_global_state(
        default_inputs_from_prepare=default_inputs,
        default_parameters_from_prepare=default_parameters,
    )
