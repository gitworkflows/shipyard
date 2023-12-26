"""Pytest plugin that spins up a single shipyard instance in the current interpreter that is shared
across the current test session.

Use in your module as follows::

    pytest_plugins = "shipyard.testing.pytest.in_memory_shipyard"

    @pytest.hookimpl()
    def pytest_configure(config):
        config.option.start_shipyard = True

You can explicitly disable starting shipyard by setting ``TEST_SKIP_SHIPYARD_START=1`` or
``TEST_TARGET=AWS_CLOUD``."""
import logging
import os
import threading

import pytest
from _pytest.config import PytestPluginManager
from _pytest.config.argparsing import Parser
from _pytest.main import Session

from shipyard import config as shipyard_config
from shipyard.config import is_env_true
from shipyard.constants import ENV_INTERNAL_TEST_RUN

LOG = logging.getLogger(__name__)
LOG.info("Pytest plugin for in-memory-shipyard session loaded.")

if shipyard_config.is_collect_metrics_mode():
    pytest_plugins = "shipyard.testing.pytest.metric_collection"


_started = threading.Event()


def pytest_addoption(parser: Parser, pluginmanager: PytestPluginManager):
    parser.addoption(
        "--start-shipyard",
        action="store_true",
        default=False,
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session: Session):
    if not session.config.option.start_shipyard:
        return

    from shipyard.testing.aws.util import is_aws_cloud

    if is_env_true("TEST_SKIP_SHIPYARD_START") or is_aws_cloud():
        LOG.info("TEST_SKIP_SHIPYARD_START is set, not starting shipyard")
        return

    from shipyard.runtime import events
    from shipyard.services import infra
    from shipyard.utils.common import safe_requests

    if is_aws_cloud():
        shipyard_config.DEFAULT_DELAY = 5
        shipyard_config.DEFAULT_MAX_ATTEMPTS = 60

    # configure
    os.environ[ENV_INTERNAL_TEST_RUN] = "1"
    safe_requests.verify_ssl = False

    _started.set()
    infra.start_infra(asynchronous=True)
    # wait for infra to start (threading event)
    if not events.infra_ready.wait(timeout=120):
        raise TimeoutError("gave up waiting for infra to be ready")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: Session):
    # last pytest lifecycle hook (before pytest exits)
    if not _started.is_set():
        return

    from shipyard.runtime import events
    from shipyard.services import infra
    from shipyard.utils.threads import start_thread

    def _stop_infra(*_args):
        LOG.info("stopping infra")
        infra.stop_infra()

    start_thread(_stop_infra)
    LOG.info("waiting for infra to stop")

    if not events.infra_stopped.wait(timeout=10):
        LOG.warning("gave up waiting for infra to stop, returning anyway")
