from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EventsRuleProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Events::Rule"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.events.resource_providers.aws_events_rule import EventsRuleProvider

        self.factory = EventsRuleProvider
