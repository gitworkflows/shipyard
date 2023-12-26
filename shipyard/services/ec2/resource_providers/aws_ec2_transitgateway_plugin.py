from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2TransitGatewayProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::TransitGateway"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_transitgateway import (
            EC2TransitGatewayProvider,
        )

        self.factory = EC2TransitGatewayProvider
