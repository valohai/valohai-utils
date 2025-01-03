"""Helper for getting information about the current execution."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from valohai.paths import get_config_path


@dataclass(frozen=True)
class ExecutionConfig:
    """Information about the current execution."""

    counter: Optional[int]
    id: Optional[str]
    title: Optional[str]


class Execution:
    @property
    def config(self) -> Optional[ExecutionConfig]:
        """
        Fetch execution configuration information.

        Returns:
            ExecutionConfig: The execution configuration information
                             or None when running locally.
        """
        config_file = Path(get_config_path()) / "execution.json"
        try:
            config = json.loads(config_file.read_bytes())
        except FileNotFoundError:
            return None

        return ExecutionConfig(
            counter=config.get("valohai.execution-counter"),
            id=config.get("valohai.execution-id"),
            title=config.get("valohai.execution-title"),
        )


execution = Execution
