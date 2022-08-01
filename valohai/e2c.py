import warnings


def set_status_detail(status_detail: str) -> None:
    try:
        from valohai.internals.api_calls import send_api_request

        send_api_request(
            endpoint="set_status_detail",
            json={"status_detail": status_detail},
        )
    except Exception as exc:
        warnings.warn(f"Status detail send failed: {exc}")
