import logging
from typing import List

from shipyard.config import HostAndPort
from shipyard.http.hypercorn import GatewayServer
from shipyard.runtime.shutdown import ON_AFTER_SERVICE_SHUTDOWN_HANDLERS
from shipyard.services.plugins import SERVICE_PLUGINS

LOG = logging.getLogger(__name__)


def serve_gateway(
    listen: HostAndPort | List[HostAndPort], use_ssl: bool, asynchronous: bool = False
):
    """
    Implementation of the edge.do_start_edge_proxy interface to start a Hypercorn server instance serving the
    ShipyardAwsGateway.
    """
    from shipyard.aws.app import ShipyardAwsGateway

    gateway = ShipyardAwsGateway(SERVICE_PLUGINS)

    # start serving gateway
    server = GatewayServer(gateway, listen, use_ssl)
    server.start()

    # with the current way the infrastructure is started, this is the easiest way to shut down the server correctly
    # FIXME: but the infrastructure shutdown should be much cleaner, core components like the gateway should be handled
    #  explicitly by the thing starting the components, not implicitly by the components.
    def _shutdown_gateway():
        LOG.debug("[shutdown] Shutting down gateway server")
        server.shutdown()

    ON_AFTER_SERVICE_SHUTDOWN_HANDLERS.register(_shutdown_gateway)

    if not asynchronous:
        server.join()

    return server._thread
