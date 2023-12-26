import pytest
import requests

from shipyard import config
from shipyard.config import in_docker
from shipyard.utils.bootstrap import ShipyardContainerServer


@pytest.mark.skipif(condition=in_docker(), reason="cannot run bootstrap tests in docker")
class TestShipyardContainerServer:
    def test_lifecycle(self):
        server = ShipyardContainerServer()
        server.container.config.ports.add(config.GATEWAY_LISTEN[0].port)

        assert not server.is_up()
        try:
            server.start()
            assert server.wait_is_up(60)

            response = requests.get("http://localhost:4566/_shipyard/health")
            assert response.ok, "expected health check to return OK: %s" % response.text
        finally:
            server.shutdown()

        server.join(30)
        assert not server.is_up()
