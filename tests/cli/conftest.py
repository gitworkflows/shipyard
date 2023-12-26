import pytest

from shipyard import config


@pytest.fixture(autouse=True)
def _setup_cli_environment(monkeypatch):
    # normally we are setting SHIPYARD_CLI in shipyard/cli/main.py, which is not actually run in the tests
    monkeypatch.setenv("SHIPYARD_CLI", "1")
    monkeypatch.setattr(config, "dirs", config.Directories.for_cli())
