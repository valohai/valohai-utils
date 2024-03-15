from __future__ import annotations

from typing import Tuple, Any
import urllib.parse
import requests
import json
import enum
import sys
import hmac
import time
import os
import re


class StrEnum(str, enum.Enum):
    pass


class WebhookException(Exception):
    pass


class RequestMethod(StrEnum):
    post = "POST"
    get = "GET"


class DataFormat(StrEnum):
    json = "json"
    urlencoded = "urlencoded"
    bytes = "bytes"


class AuthType(StrEnum):
    static_token = "static_token"  # noqa
    hmac = "hmac"


class RequestNamespace(StrEnum):
    query = "query"
    header = "header"


# This is a subset of all supported HMAC algorithms.
# You can check the full set of HMAC algorithms that can be used on this system from
# `hashlib.algorithms_available`.
class HMACAlgorithm(StrEnum):
    sha1 = "sha1"
    sha256 = "sha256"
    sha512 = "sha512"


class TimestampType(StrEnum):
    none = "none"
    unix_second = "unix_s"
    unix_millisecond = "unix_ms"


class Webhook:
    """Creates requests that can be sent to most webhook endpoints,
    supporting HMAC and static token authentication.
    """

    def __init__(
        self,
        url: str,
        *,
        title: str = "",
        method: RequestMethod = RequestMethod.post,
        auth_type: AuthType | None = None,
        auth_namespace: RequestNamespace = RequestNamespace.header,
        auth_key: str = "Authorization",
        auth_secret_prefix: str = "",
        auth_secret: str | None = None,
        auth_algorithm: HMACAlgorithm | str | None = None,
        hmac_format: bytes = b"%(body)s",
        timestamp: TimestampType = TimestampType.none,
        timestamp_namespace: RequestNamespace = RequestNamespace.header,
        timestamp_key: str = "X-Timestamp",
    ) -> None:
        self.url = url
        self.title = title
        self.method = method
        self.auth_type = auth_type
        self.auth_namespace = auth_namespace
        self.auth_key = auth_key
        self.auth_secret_prefix = auth_secret_prefix
        self.auth_secret = auth_secret
        self.auth_algorithm = auth_algorithm
        self.hmac_format = hmac_format
        self.timestamp_type = timestamp
        self.timestamp: int | None
        if timestamp == TimestampType.unix_second:
            self.timestamp = int(time.time())
        elif timestamp == TimestampType.unix_millisecond:
            self.timestamp = int(time.time() * 1000)
        else:
            self.timestamp = None
        self.timestamp_namespace = timestamp_namespace
        self.timestamp_key = timestamp_key

    def __str__(self) -> str:
        if self.title:
            url_domain = urllib.parse.urlparse(self.url).netloc
            return f"Webhook ({url_domain}): {self.title}"
        return f"Webhook: {self.url}"

    def hmac_authentication_header(self, encoded_request_data: bytes) -> str:
        formatted_data = self.hmac_format % {
            b"body": encoded_request_data,
            b"timestamp": self.timestamp,
        }
        secret_str = self.resolve_auth_secret()
        if secret_str is None:
            raise WebhookException("Must supply a secret to authenticate with HMAC")

        if isinstance(self.auth_algorithm, HMACAlgorithm):
            algorithm = self.auth_algorithm.value
        elif isinstance(self.auth_algorithm, str):
            algorithm = self.auth_algorithm
        else:
            raise WebhookException(
                "Must specify a HMAC algorithm to authenticate with HMAC"
            )

        sig = hmac.new(
            key=secret_str.encode(),
            msg=formatted_data,
            digestmod=algorithm,
        ).hexdigest()
        return sig

    def resolve_auth_secret(self) -> str | None:
        if self.auth_secret is None:
            return None
        match = re.match(r"{env:(.*)}", self.auth_secret)
        if match is not None:
            env_key = match.group(1)
            from_env = os.getenv(env_key)
            if from_env is None:
                raise WebhookException(
                    f"Could not find required environment variable {env_key} specified as secret value"
                )
            return from_env
        return self.auth_secret

    def get_hmac_headers(self, encoded_data: bytes | None) -> dict[str, str]:
        if not self.resolve_auth_secret():
            raise WebhookException("Must supply auth secret if using HMAC auth type")
        if self.auth_namespace != RequestNamespace.header:
            raise WebhookException("HMAC authentication can only be set as a header")
        if encoded_data is None:
            raise WebhookException("Must have POST data for HMAC")
        return {
            self.auth_key: f"{self.auth_secret_prefix}{self.hmac_authentication_header(encoded_data)}"
        }

    def get_static_token_query_and_headers(
        self,
    ) -> Tuple[dict[str, str], dict[str, str]]:
        if not self.resolve_auth_secret():
            raise WebhookException(
                "Must supply auth secret if using static token auth type"
            )
        auth_data = {
            self.auth_key: f"{self.auth_secret_prefix}{self.resolve_auth_secret()}"
        }
        if self.auth_namespace == RequestNamespace.query:
            query = auth_data
            headers = {}
        elif self.auth_namespace == RequestNamespace.header:
            query = {}
            headers = auth_data
        else:
            raise WebhookException(
                "Must place static token in either the query string or headers"
            )
        return query, headers

    def get_auth_query_and_headers(
        self, encoded_data: bytes | None = None
    ) -> Tuple[dict[str, str], dict[str, str]]:
        query: dict[str, str]
        headers: dict[str, str]

        if self.auth_type == AuthType.hmac:
            query = {}
            headers = self.get_hmac_headers(encoded_data)
        elif self.auth_type == AuthType.static_token:
            query, headers = self.get_static_token_query_and_headers()
        else:
            query = {}
            headers = {}

        if self.timestamp_type != TimestampType.none:
            if self.timestamp_namespace == RequestNamespace.header:
                headers[self.timestamp_key] = str(self.timestamp)
            else:
                query[self.timestamp_key] = str(self.timestamp)

        return query, headers

    def handle_response(self, response: requests.Response) -> requests.Response:
        try:
            response.raise_for_status()
        except requests.RequestException as req_exc:
            sys.stderr.write(
                f"Webhook request to {self.url} reported error status {response.status_code}\n"
            )
            sys.stderr.write("--- Start Error Response Content ---\n")
            sys.stderr.write(response.content.decode())
            sys.stderr.write("\n--- End Error Response Content ---\n")
            raise WebhookException(
                f"{self.url}: Response error {response.status_code}"
            ) from req_exc

        return response

    def post(
        self,
        data: dict[str, Any] | bytes,
        *,
        data_format: DataFormat = DataFormat.json,
        content_type: str | None = None,
    ) -> requests.Response:
        if self.method != RequestMethod.post:
            raise WebhookException(
                f"This webhook's request method is {self.method}, not post"
            )
        encoded_data: bytes
        if data_format == DataFormat.json:
            encoded_data = json.dumps(data).encode()
            content_type = "application/json"
        elif data_format == DataFormat.urlencoded:
            if not isinstance(data, dict):
                raise WebhookException("Urlencoded data must be a dict")
            encoded_data = urllib.parse.urlencode(data).encode()
            content_type = "application/x-www-form-urlencoded"
        elif data_format == DataFormat.bytes:
            if not isinstance(data, bytes):
                raise WebhookException("must send bytes if format is bytes")
            if content_type is None:
                raise WebhookException("must set content_type if sending bytes")
            encoded_data = data
        else:
            raise WebhookException(f"unknown data format {format} requested")

        query, headers = self.get_auth_query_and_headers(encoded_data)
        headers["Content-Type"] = content_type
        encoded_query = urllib.parse.urlencode(query)

        response: requests.Response = requests.post(
            f"{self.url}?{encoded_query}", data=encoded_data, headers=headers
        )

        return self.handle_response(response)

    def get(self, query_params: dict[str, Any] | None = None) -> requests.Response:
        if self.method != RequestMethod.post:
            raise WebhookException(
                f"This webhook's request method is {self.method}, not get"
            )

        query, headers = self.get_auth_query_and_headers()
        if query_params is not None:
            query_params.update(query)
        else:
            query_params = query
        encoded_query = urllib.parse.urlencode(query_params)

        response: requests.Response = requests.post(
            f"{self.url}?{encoded_query}", headers=headers
        )

        return self.handle_response(response)
