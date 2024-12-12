"""Execution output properties helper.

The properties are saved in a `valohai.metadata.jsonl` file in the outputs directory
in JSON lines format.
"""

import json
from pathlib import Path
from typing import Any, Union, Dict, Optional

from valohai.paths import get_outputs_path

File = Union[str, Path]  # path to the file (relative to outputs directory)
Properties = Dict[str, Any]  # metadata properties for a file
FilesProperties = Dict[File, Properties]


class OutputProperties:
    """Helper for setting properties for output files."""

    _files_properties: FilesProperties

    def __init__(self) -> None:
        self._files_properties = {}
        self.properties_file = Path(get_outputs_path()) / "valohai.metadata.jsonl"

    def __enter__(self) -> "OutputProperties":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._save()

    def set(self, *, file: File, properties: Optional[Properties] = None) -> None:
        """
        Set properties for a file.
        If the file already has properties, they will be overwritten.

        Args:
            file: The path to the file (relative to the execution outputs root directory).
            properties: The metadata properties for the file.
        """
        props: Properties = properties or {}
        self._files_properties[str(file)] = props

    def _save(self):
        Path(self.properties_file).write_text(
            "".join(
                format_line(file_path, file_metadata)
                for file_path, file_metadata in self._files_properties.items()
            )
        )


output_properties = OutputProperties


def format_line(file_path: File, file_metadata: Properties) -> str:
    """Format metadata for an output file into a format Valohai understands.

    Args:
        file_path: The path to the file (relative to the execution outputs root directory).
        file_metadata: The metadata for the file.
    """
    return (
        json.dumps(
            {
                "file": file_path,
                "metadata": file_metadata,
            }
        )
        + "\n"
    )
