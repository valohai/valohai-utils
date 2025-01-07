import json
from pathlib import Path

import pytest

import valohai
from valohai.paths import get_config_path

# execution configuration example
EXAMPLE_CONFIG = {
    "valohai.commit-identifier": "~8603a0246c0397770945439249084fa514eab09548a88dfcb16a019dfe420301",
    "valohai.creator-email": None,
    "valohai.creator-id": 1,
    "valohai.creator-name": "test-user",
    "valohai.environment-id": "0189ba6d-b1f5-4b64-1a08-9ff09f447034",
    "valohai.environment-name": "The Default Environment",
    "valohai.environment-slug": "default",
    "valohai.execution-counter": 42,
    "valohai.execution-ctime": "2024-12-30T13:58:46.832605+00:00",
    "valohai.execution-duration": None,
    "valohai.execution-id": "019417dc-b12f-0021-c074-87370badadef",
    "valohai.execution-image": "ghcr.io/astral-sh/uv:python3.12-bookworm-slim",
    "valohai.execution-qtime": None,
    "valohai.execution-status": "created",
    "valohai.execution-step": "exec-step-name",
    "valohai.execution-tags": [],
    "valohai.execution-title": "example execution title",
    "valohai.project-id": "01931b1d-9db0-0021-c074-87370badadef",
    "valohai.project-name": "test-org/test-project",
}


def test_config_does_not_exist():
    config_path = Path(get_config_path())
    assert (
        not config_path.exists()
    ), "Config file should not exist by default when not running in Valohai"

    # try reading a non-existent config file
    assert valohai.execution().config is None, "Execution should not exist"


def test_get_config(fake_config):
    fake_config.write_text(json.dumps(EXAMPLE_CONFIG))

    config = valohai.execution().config
    assert config is not None, "Execution config should exist"

    assert config.id == EXAMPLE_CONFIG["valohai.execution-id"]
    assert config.title == EXAMPLE_CONFIG["valohai.execution-title"]
    assert config.counter == EXAMPLE_CONFIG["valohai.execution-counter"]


@pytest.fixture
def fake_config(tmp_path, monkeypatch) -> Path:
    """Create and use a fake execution configuration file."""
    config_file = tmp_path / "execution.json"
    # patch the config path to point to the fake file
    monkeypatch.setenv("VH_CONFIG_DIR", str(tmp_path))

    return config_file
