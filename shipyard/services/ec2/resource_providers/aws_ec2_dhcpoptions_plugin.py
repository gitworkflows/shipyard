from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2DHCPOptionsProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::DHCPOptions"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_dhcpoptions import (
            EC2DHCPOptionsProvider,
        )

        self.factory = EC2DHCPOptionsProvider
