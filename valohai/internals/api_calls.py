from typing import TYPE_CHECKING, Any

from valohai import paths
from valohai.internals import json_utils

if TYPE_CHECKING:
    import requests


def get_api_requests_kwargs(endpoint: str) -> dict[str, Any]:
    """
    Get the "presigned call" dict for a given endpoint from the
    API JSON configuration file.  Will happily throw all sorts of
    exceptions e.g. if the API JSON file is missing or malformed.
    """
    api_config = json_utils.load_file(paths.get_api_config_path())
    value = api_config.get(endpoint)
    if not (isinstance(value, dict) and value.get("url")):
        raise ValueError(f"Invalid API config for {endpoint}")
    return value


def send_api_request(
    endpoint: str,
    **requests_kwargs: Any,
) -> "requests.Response":
    """
    Send an API request to the named endpoint.

    Will happily throw all sorts of exceptions; it is the caller's
    responsibility to handle them in a suitable way.

    :param endpoint: The endpoint to send the request to.  Will be
                     looked up in the API JSON configuration file.
    :param requests_kwargs: Any keyword arguments to pass to the
                            requests.request() function.  You can expect
                            `url` and `method` and likely `headers` to
                            have been set for you.
    """
    import requests

    requests_config = get_api_requests_kwargs(endpoint)
    requests_config.update(requests_kwargs)
    resp = requests.request(**requests_config)
    resp.raise_for_status()
    return resp
