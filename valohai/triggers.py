from __future__ import annotations

from valohai.webhooks import Webhook, WebhookException


class TriggerException(WebhookException):
    pass


class Triggers:
    def __init__(self) -> None:
        self._triggers: dict[str, Webhook] = {}

    def __call__(self, title_or_uuid: str, *, required: bool = True) -> Webhook | None:
        if title_or_uuid in self._triggers:
            return self._triggers[title_or_uuid]

        response = None
        failure_detail: str | None = None
        failure_exception: Exception | None = None
        try:
            from valohai.internals.api_calls import send_api_request

            response = send_api_request(
                endpoint="trigger_catalog", params={"q": title_or_uuid}
            )
        except FileNotFoundError as exc:
            failure_detail = "Not in a compatible Valohai execution"
            failure_exception = exc
        except Exception as exc:
            failure_detail = "Exception raised when looking up trigger"
            failure_exception = exc

        if not response:
            if not required:
                return None
            raise TriggerException(
                f"Required trigger could not be found: {failure_detail}",
            ) from failure_exception

        manifest = response.json()["manifest"]
        self._triggers[title_or_uuid] = webhook = Webhook(**manifest)
        return webhook


triggers = Triggers()
