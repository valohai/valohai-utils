import pytest
from typing import Callable

from valohai.webhooks import (
    Webhook,
    AuthType,
    HMACAlgorithm,
    TimestampType,
    RequestNamespace,
)

VALID_WEBHOOK_CONFIGS = [
    (
        "just_url",
        {"url": "https://example.org/"},
        lambda request: request.url == "https://example.org/",
    ),
    (
        "basic_hmac",
        {
            "url": "https://example.org/",
            "auth_type": AuthType.hmac,
            "auth_algorithm": HMACAlgorithm.sha256,
            "auth_secret": "foobar",
        },
        lambda request: request.headers["Authorization"]
        == "15b944e3ab6db92072ebef4cc272912905c8b0295ec44d826b09949b10ee2510",
    ),
    (
        "hmac_customized",
        {
            "url": "https://example.org/",
            "auth_type": AuthType.hmac,
            "auth_algorithm": HMACAlgorithm.sha256,
            "auth_secret": "foobar",
            "auth_secret_prefix": "v0=",
            "auth_key": "X-Special-HMAC",
        },
        lambda request: request.headers["X-Special-HMAC"]
        == "v0=15b944e3ab6db92072ebef4cc272912905c8b0295ec44d826b09949b10ee2510",
    ),
    (
        "hmac_with_timestamp",
        {
            "url": "https://example.org/",
            "auth_type": AuthType.hmac,
            "auth_algorithm": HMACAlgorithm.sha256,
            "auth_secret": "foobar",
            "auth_secret_prefix": "v123=",
            "auth_key": "X-Special-Timestamped-HMAC",
            "timestamp": TimestampType.unix_second,
            "timestamp_key": "X-Special-Timestamp",
            "hmac_format": b"v123:%(body)s:%(timestamp)d",
        },
        lambda request: "X-Special-Timestamp" in request.headers
        and "X-Special-Timestamped-HMAC" in request.headers,
    ),
    (
        "secret_from_env",
        {
            "url": "https://example.org/",
            "auth_type": AuthType.static_token,
            "auth_namespace": RequestNamespace.query,
            "auth_key": "token",
            "auth_secret": "{env:FOOBAR}",
        },
        lambda request: request.url.endswith("?token=supersecret"),
    ),
]


@pytest.mark.parametrize(
    "webhook_kwargs, test",
    [
        pytest.param(config, test, id=name)
        for name, config, test in VALID_WEBHOOK_CONFIGS
    ],
)
def test_webhook_creates_request_successfully(
    requests_mock, monkeypatch, webhook_kwargs: dict, test: Callable
):
    monkeypatch.setenv("FOOBAR", "supersecret")
    requests_mock.post("https://example.org/", json={"status": "ok"})

    webhook = Webhook(**webhook_kwargs)
    webhook.post({"foo": "bar"})

    assert requests_mock.called
    assert test(request=requests_mock.last_request)
