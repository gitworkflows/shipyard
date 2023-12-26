from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2RouteProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::Route"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_route import EC2RouteProvider

        self.factory = EC2RouteProvider
