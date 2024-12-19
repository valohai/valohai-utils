import os

import pytest

from valohai.internals import global_state

from .valohai_test_environment import ValohaiTestEnvironment


@pytest.fixture
def vte(tmpdir):
    return ValohaiTestEnvironment(root_dir=str(tmpdir.mkdir("valohai")))


@pytest.fixture
def use_test_config_dir(vte, monkeypatch):
    vte.build()
    monkeypatch.setenv("VH_CONFIG_DIR", str(vte.config_path))
    monkeypatch.setenv("VH_INPUTS_DIR", str(vte.inputs_path))
    monkeypatch.setenv("VH_OUTPUTS_DIR", str(vte.outputs_path))

    # pytest carries global state between tests if we don't flush it
    global_state.flush_global_state()


@pytest.fixture
def use_distributed_config(request, monkeypatch):
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_parsing_distributed",
        request.param,
    )
    with monkeypatch.context() as m:
        from valohai.distributed import Distributed

        m.setattr(Distributed, "_get_config_path", lambda self: config_path)
        yield config_path
    global_state.flush_global_state()


@pytest.fixture
def outputs_path(tmpdir, monkeypatch):
    outputs_path = os.path.join(str(tmpdir), "outputs")
    monkeypatch.setenv("VH_OUTPUTS_DIR", outputs_path)
    return outputs_path


@pytest.fixture
def output_files(outputs_path):
    return create_files(outputs_path)


def create_files(path):
    os.makedirs(os.path.join(path, "folder"))
    os.makedirs(os.path.join(path, "folder2"))

    outputs = [
        os.path.join(path, "test1.bin"),
        os.path.join(path, "test2.bin"),
        os.path.join(path, "folder", "picture.jpg"),
        os.path.join(path, "folder", "picturetoo.jpg"),
        os.path.join(path, "folder", "imapng.png"),
        os.path.join(path, "folder2", "asdf.dat"),
    ]

    for output in outputs:
        with open(output, "wb") as f:
            f.write(os.urandom(1000))

    return outputs
