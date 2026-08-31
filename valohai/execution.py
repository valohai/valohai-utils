"""Helper for getting information about the current execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from valohai.internals import json_utils
from valohai.paths import get_config_path


@dataclass(frozen=True)
class ExecutionConfig:
    """Information about the current execution."""

    counter: int | None
    id: str | None
    title: str | None


class Execution:
    @property
    def config(self) -> ExecutionConfig | None:
        """
        Fetch execution configuration information.

        Returns:
            ExecutionConfig: The execution configuration information
                             or None when running locally.
        """
        config_file = Path(get_config_path()) / "execution.json"
        try:
            config = json_utils.loads(config_file.read_bytes())
        except FileNotFoundError:
            return None

        return ExecutionConfig(
            counter=config.get("valohai.execution-counter"),
            id=config.get("valohai.execution-id"),
            title=config.get("valohai.execution-title"),
        )


execution = Execution
