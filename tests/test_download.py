import os
import sys
import uuid
import json

import pytest

import valohai
from valohai.internals.inputs import get_input_info, get_input_vfs
from valohai_cli import settings as settings_module


def test_download(tmpdir, monkeypatch, requests_mock):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)

    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz"
    )
    requests_mock.get(
        "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz"
    )

    inputs = {
        "example": "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "mnist": [
            "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz",
            "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz",
        ],
    }

    monkeypatch.setattr(sys, "argv", ["myscript.py"])
    valohai.prepare(step="test", default_inputs=inputs)

    # These calls will trigger downloads
    get_input_vfs("example")
    get_input_vfs("mnist")

    assert (
        get_input_info("example").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz"
    )
    assert (
        get_input_info("mnist").files[0].uri
        == "https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz"
    )
    assert (
        get_input_info("mnist").files[1].uri
        == "https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz"
    )
    assert requests_mock.call_count == 3

    assert os.path.isfile(
        os.path.join(inputs_dir, "example", "t10k-images-idx3-ubyte.gz")
    )
    assert os.path.isfile(
        os.path.join(inputs_dir, "mnist", "train-images-idx3-ubyte.gz")
    )
    assert os.path.isfile(
        os.path.join(inputs_dir, "mnist", "train-labels-idx1-ubyte.gz")
    )

    # Second time around, the file should be cached and not trigger any more downloads
    get_input_vfs("mnist")
    get_input_vfs("example")

    assert requests_mock.call_count == 3


@pytest.mark.parametrize(
    "datum_name",
    [
        "01941935-832f-16d4-af69-6a9bf6bf4df6",
        "my_models_alias",
    ],
)
def test_datum_url_download(tmpdir, monkeypatch, requests_mock, datum_name):
    inputs_dir = str(tmpdir.mkdir("inputs"))
    project_dir = str(tmpdir.mkdir("project"))
    monkeypatch.setenv("VH_INPUTS_DIR", inputs_dir)

    project_id = "018a5fc7-02f8-d42d-a22b-cb6ffe20919e"
    datum_id = "01941935-832f-16d4-af69-6a9bf6bf4df6"
    datum_alias = "my_models_alias"
    vh_host = "https://app.valohai.com"
    filename = "t10k-images-idx3-ubyte.gz"
    file_sha256 = "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589"

    # Final file to download
    requests_mock.get(
        f"https://valohai-mnist.s3.amazonaws.com/{filename}",
        text="abcd",
    )
    # Project API is required to log in to CLI
    requests_mock.get(
        f"{vh_host}/api/v0/projects/{project_id}/",
        json={
            "name": "Good Project",
            "id": project_id,
        },
    )
    # Datum by alias lookup API
    requests_mock.get(
        f"{vh_host}/api/v0/datum-aliases/resolve/?name={datum_alias}&project={project_id}",
        json={
            "datum": {
                "name": filename,
                "id": datum_id,
                "sha256": file_sha256,
            }
        },
    )
    # Datum by exact ID API
    requests_mock.get(
        f"{vh_host}/api/v0/data/{datum_id}",
        json={
            "name": filename,
            "id": datum_id,
            "sha256": file_sha256,
        },
    )
    # Datum download API
    requests_mock.get(
        f"{vh_host}/api/v0/data/{datum_id}/download/",
        json={"url": f"https://valohai-mnist.s3.amazonaws.com/{filename}"},
    )

    # Set up CLI -- it is required for datum URL downloads
    cli_settings = settings_module.Settings()
    cli_settings.overrides["host"] = vh_host
    cli_settings.overrides["token"] = "a token"
    monkeypatch.setattr(settings_module, "settings", cli_settings)

    cli_settings.set_override_project(
        project_id=project_id,
        directory=project_dir,
        mode="remote",
    )

    inputs = {
        "example": f"datum://{datum_name}",
    }

    monkeypatch.setattr(sys, "argv", ["myscript.py"])
    valohai.prepare(step="test", default_inputs=inputs)

    # This triggers the download
    get_input_vfs("example")

    assert os.path.isfile(os.path.join(inputs_dir, "example", filename))
    assert requests_mock.call_count == 4


def test_download_by_input_id(vte, use_test_config_dir, requests_mock):
    filename = "t10k-images-idx3-ubyte.gz"
    input_id = str(uuid.uuid4())
    input_request_url = "http://example.com/input-request/"
    download_url = f"https://valohai-mnist.s3.amazonaws.com/{filename}"

    # Setup:
    # ---

    # Write a config file that contains an on-demand input
    inputs_config = {
        "on-demand": {
            "input_id": input_id,
            "files": [
                {
                    "path": f"{vte.inputs_path}/{filename}",
                    "name": filename,
                    "uri": f"s3://valohai-mnist.s3.amazonaws.com/{filename}",
                    "size": 0,
                    "input_id": input_id,
                    "storage_uri": f"s3://valohai-mnist.s3.amazonaws.com/{filename}",
                    "download_intent": "on-demand",
                },
            ],
        }
    }
    with open(os.path.join(vte.config_path, "inputs.json"), "w") as inputs_f:
        json.dump(inputs_config, inputs_f)

    # Write a config file that contains an input_request API endpoint
    api_config = {
        "input_request": {
            "url": input_request_url,
            "method": "POST",
        },
    }
    with open(os.path.join(vte.config_path, "api.json"), "w") as api_f:
        json.dump(api_config, api_f)

    # Set up requests_mock
    requests_mock.post(
        input_request_url,
        json=[
            {
                "name": "on-demand",
                "files": [
                    {
                        "input_id": input_id,
                        "url": download_url,
                        "original_uri": f"s3://valohai-mnist.s3.amazonaws.com/{filename}",
                        "filename": filename,
                        "download_intent": "on-demand",
                    },
                ],
            },
        ],
    )
    requests_mock.get(download_url, text="I was downloaded by valohai-utils")

    # Assumptions
    # ---
    # The file does not exist before it is accessed by valohai-utils
    local_filename = os.path.join(vte.inputs_path, "on-demand", filename)
    assert not os.path.isfile(local_filename)

    # Trigger the download
    # ---
    get_input_vfs("on-demand")

    # Assertions
    # ---

    # We can tell it was downloaded the way we expected it to be
    assert requests_mock.call_count == 2
    first_rq, second_rq = requests_mock.request_history
    assert first_rq.url == f"{input_request_url}?inputs={input_id}"
    assert second_rq.url == download_url

    # The file now exists and contains the downloaded data
    assert os.path.isfile(local_filename)
    with open(local_filename, "r") as local_file:
        file_contents = local_file.read()
    assert file_contents == "I was downloaded by valohai-utils"
