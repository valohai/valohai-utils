import os


def is_running_in_valohai() -> bool:
    return bool(os.environ.get("VH_JOB_ID"))
