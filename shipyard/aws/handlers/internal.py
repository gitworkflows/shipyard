"""Handler for routing internal shipyard resources under /_shipyard."""
import logging

from werkzeug.exceptions import NotFound

from shipyard import constants
from shipyard.http import Response
from shipyard.runtime import events
from shipyard.services.internal import ShipyardResources

from ..api import RequestContext
from ..chain import Handler, HandlerChain

LOG = logging.getLogger(__name__)


class ShipyardResourceHandler(Handler):
    """
    Adapter to serve ShipyardResources as a Handler.
    """

    resources: ShipyardResources

    def __init__(self, resources: ShipyardResources = None) -> None:
        from shipyard.services.internal import get_internal_apis

        self.resources = resources or get_internal_apis()

    def __call__(self, chain: HandlerChain, context: RequestContext, response: Response):
        try:
            # serve
            response.update_from(self.resources.dispatch(context.request))
            chain.stop()
        except NotFound:
            path = context.request.path
            if path.startswith(constants.INTERNAL_RESOURCE_PATH + "/"):
                # only return 404 if we're accessing an internal resource, otherwise fall back to the other handlers
                LOG.warning("Unable to find resource handler for path: %s", path)
                chain.respond(404)


class RuntimeShutdownHandler(Handler):
    def __call__(self, chain: HandlerChain, context: RequestContext, response: Response):
        if events.infra_stopped.is_set():
            chain.respond(503)
        elif events.infra_stopping.is_set():
            # if we're in the process of shutting down the infrastructure, only accept internal calls
            if not context.is_internal_call:
                chain.respond(503)
