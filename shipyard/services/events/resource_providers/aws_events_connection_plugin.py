from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EventsConnectionProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Events::Connection"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.events.resource_providers.aws_events_connection import (
            EventsConnectionProvider,
        )

        self.factory = EventsConnectionProvider
