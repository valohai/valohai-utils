import os


def is_running_in_valohai() -> bool:
    return bool(os.environ.get("VH_JOB_ID"))


def is_valohai_deployment() -> bool:
    return bool(os.environ.get('VALOHAI_PORT') or os.path.exists("/valohai/valohai-metadata.json"))
