import json
from typing import Any

import requests

from valohai import paths


def get_api_requests_kwargs(endpoint: str):
    """
    Get the "presigned call" dict for a given endpoint from the
    API JSON configuration file.  Will happily throw all sorts of
    exceptions e.g. if the API JSON file is missing or malformed.
    """
    with open(paths.get_api_config_path()) as json_file:
        api_config = json.load(json_file)
    value = api_config.get(endpoint)
    if not (isinstance(value, dict) and value.get("url")):
        raise ValueError(f"Invalid API config for {endpoint}")
    return value


def send_api_request(
    endpoint: str,
    **requests_kwargs: Any,
):
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
    requests_config = get_api_requests_kwargs(endpoint)
    requests_config.update(requests_kwargs)
    resp = requests.request(**requests_config)
    resp.raise_for_status()
    return resp
