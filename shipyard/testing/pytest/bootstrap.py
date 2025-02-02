import pytest

from shipyard import config


@pytest.fixture(scope="session", autouse=True)
def setup_host_config_dirs():
    config.dirs.mkdirs()
