import warnings


def set_status_detail(status_detail: str) -> None:
    """
    Attempt to set the status detail of the current execution.
    """
    try:
        from valohai.internals.api_calls import send_api_request

        send_api_request(
            endpoint="set_status_detail",
            json={"status_detail": status_detail},
        )
    except FileNotFoundError:  # No API configuration file, no need to warn
        pass
    except Exception as exc:
        warnings.warn(f"Status detail send failed: {exc}")
