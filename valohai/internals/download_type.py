from enum import Enum


class DownloadType(Enum):
    NEVER = 0
    OPTIONAL = 1  # Only download when not found from cache
    ALWAYS = 2
