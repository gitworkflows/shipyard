from _pytest.config import Config

from shipyard import config as shipyard_config
from shipyard import constants


def pytest_configure(config: Config):
    # FIXME: note that this should be the same as in tests/aws/conftest.py since both are currently run in
    #  the same CI test step, but only one shipyard instance is started for both.
    config.option.start_shipyard = True
    shipyard_config.FORCE_SHUTDOWN = False
    shipyard_config.GATEWAY_LISTEN = shipyard_config.UniqueHostAndPortList(
        [shipyard_config.HostAndPort(host="0.0.0.0", port=constants.DEFAULT_PORT_EDGE)]
    )
