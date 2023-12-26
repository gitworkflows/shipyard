from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2SecurityGroupProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::SecurityGroup"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_securitygroup import (
            EC2SecurityGroupProvider,
        )

        self.factory = EC2SecurityGroupProvider
