from __future__ import annotations
import warnings

from valohai.webhooks import Webhook


class Triggers:
    def __init__(self) -> None:
        self._triggers: dict[str, Webhook] = {}

    def __call__(self, title_or_uuid: str, *, required: bool = True) -> Webhook | None:
        if title_or_uuid in self._triggers:
            return self._triggers[title_or_uuid]

        response = None
        try:
            from valohai.internals.api_calls import send_api_request

            response = send_api_request(
                endpoint="trigger_catalog", params={"q": title_or_uuid}
            )
        except FileNotFoundError:  # No API configuration file, no need to warn
            pass
        except Exception as exc:
            warnings.warn(f"Trigger catalog query failed: {exc}")

        if not response:
            if not required:
                return None
            raise ValueError("Could not query for a required trigger")

        manifest = response.json()["manifest"]
        self._triggers[title_or_uuid] = webhook = Webhook(**manifest)
        return webhook


triggers = Triggers()
