from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class Route53HealthCheckProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Route53::HealthCheck"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.route53.resource_providers.aws_route53_healthcheck import (
            Route53HealthCheckProvider,
        )

        self.factory = Route53HealthCheckProvider
