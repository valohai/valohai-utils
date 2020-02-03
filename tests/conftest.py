import pytest
from .valohai_test_environment import ValohaiTestEnvironment


@pytest.fixture
def vte(tmpdir):
    return ValohaiTestEnvironment(root_dir=str(tmpdir.mkdir("valohai")))


@pytest.fixture
def use_test_config_dir(vte, monkeypatch):
    vte.build()
    monkeypatch.setenv("VH_CONFIG_DIR", str(vte.config_path))
    monkeypatch.setenv("VH_INPUT_DIR", str(vte.inputs_path))
    monkeypatch.setenv("VH_OUTPUT_DIR", str(vte.outputs_path))
