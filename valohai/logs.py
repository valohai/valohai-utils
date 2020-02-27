import json
import sys

from valohai.internals.global_state import partial_logs

_supported_types = [int, float]


def _get_serializable(name, value):
    if isinstance(value, (int, str, float)):
        return {str(name): value}

    print(f"Warning: Value of the logged item ({name}) is not of the expected type (int, str, float).", file=sys.stderr)
    return None


def log(name, value):
    """Log name/value pair into standard output using Valohai supported format.

    See log_partial() for printing out multiple variables inside your training loop.

    :param name: Name of the variable being logged (example: accuracy)
    :param value: Value of the logged variable

    """
    serializable = _get_serializable(name, value)
    if serializable:
        print(json.dumps(serializable))


def log_partial(name, value):
    """Log a single name/value pair to be flushed into standard output later as batch.

    For a repeating iteration like a machine learning training loop, Valohai expects
    all logged values to be printed as a batch.

    Example:
        valohai.log_partial("epoch", 12)
        valohai.log_partial("accuracy", 0.54)
        valohai.log_partial("loss", 0.123)
        valohai.flush_logs()

    :param name: Name of the variable being logged (example: learning_rate)
    :param value: Value of the logged variable

    """
    serializable = _get_serializable(name, value)
    if serializable:
        partial_logs.update(serializable)


def flush_logs():
    """Flush all the partial logs into standard as a batch.

    For a repeating iteration like a machine learning training loop, Valohai expects
    all logged values to be printed as single batch.

    Example:
        valohai.log_partial("epoch", 12)
        valohai.log_partial("accuracy", 0.54)
        valohai.log_partial("loss", 0.123)
        valohai.flush_logs()

    """
    if partial_logs:
        print(json.dumps(partial_logs))
        partial_logs.clear()
