from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2VPCProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::VPC"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_vpc import EC2VPCProvider

        self.factory = EC2VPCProvider
