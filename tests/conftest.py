import os

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


@pytest.fixture
def outputs_path(tmpdir, monkeypatch):
    outputs_path = os.path.join(str(tmpdir), "outputs")
    monkeypatch.setenv("VH_OUTPUTS_DIR", outputs_path)
    return outputs_path


@pytest.fixture
def output_files(outputs_path):
    os.makedirs(os.path.join(outputs_path, "folder"))
    os.makedirs(os.path.join(outputs_path, "folder2"))

    outputs = [
        os.path.join(outputs_path, "test1.bin"),
        os.path.join(outputs_path, "test2.bin"),
        os.path.join(outputs_path, "folder", "picture.jpg"),
        os.path.join(outputs_path, "folder", "picturetoo.jpg"),
        os.path.join(outputs_path, "folder", "imapng.png"),
        os.path.join(outputs_path, "folder2", "asdf.dat"),
    ]

    for output in outputs:
        with open(output, 'wb') as f:
            f.write(os.urandom(1000))

    return outputs
