import json
import os
import shlex
from typing import Any, Dict, List, Union

NotebookDict = Dict[str, Any]

# TODO: This file is a copy-pasta from https://github.com/valohai/jupyhai
# TODO: DRY between libs


def parse_ipynb(content_or_str: Union[str, NotebookDict]) -> NotebookDict:
    """
    "Smartly" parse content that contains a notebook.
    * If a string, it's first JSON deserialized.
    * If it's a "wrapped" dict (i.e. contains "type" == "notebook" and "content"), unwraps the content
    * Asserts the content smells like a notebook ("nbformat")
    :param content: See above.
    :return: Notebook data.
    """
    if isinstance(content_or_str, str):
        content = json.loads(content_or_str)
    else:
        content = content_or_str
    if not isinstance(content, dict):
        raise ValueError("Ipynb not a dict")
    if content.get("type") == "notebook":
        content = content["content"]

    nbformat = content.get("nbformat")
    if not isinstance(nbformat, int):
        raise ValueError("Nbformat value %s invalid" % nbformat)
    return dict(content)


def get_notebook_source_code(contents: NotebookDict) -> str:
    source = [
        cell["source"] for cell in contents["cells"] if cell["cell_type"] == "code"
    ]

    # Some notebook versions store it as list of rows already. Some as single string.
    source = [row if isinstance(row, list) else row.split("\n") for row in source]

    # Even when it was a list, the linefeeds are still there.
    source = [row.rstrip() for sublist in source for row in sublist]

    # Strip magics like "!pip install tensorflow"
    source = [row for row in source if not row.startswith("!")]

    return "\n".join(source)


def get_notebook_command(notebook_relative_path: str) -> List[str]:
    notebook_dir, notebook_name = os.path.split(notebook_relative_path)
    papermill_command = " ".join(
        [
            "papermill -k python3 -f /valohai/config/parameters.yaml",
            shlex.quote(
                "/valohai/repository/{}".format(
                    notebook_relative_path.replace(os.sep, "/")
                )
            ),
            shlex.quote(
                "/valohai/outputs/{}".format(notebook_name.replace(os.sep, "/"))
            ),
        ]
    )
    return ["pip install -r requirements.txt", papermill_command]
