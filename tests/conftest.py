import os

import pytest

FIXTURES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'fixtures'))


@pytest.fixture
def use_test_config_dir(monkeypatch):
    monkeypatch.setenv('VH_CONFIG_DIR', os.path.join(FIXTURES_PATH, 'config'))
