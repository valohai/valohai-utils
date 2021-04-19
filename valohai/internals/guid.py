import time
import uuid

_execution_guid = None


def get_execution_guid() -> str:
    global _execution_guid
    if not _execution_guid:
        _execution_guid = f'{time.strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex[:6]}'
    return _execution_guid
