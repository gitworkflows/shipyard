from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class EC2TransitGatewayAttachmentProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::EC2::TransitGatewayAttachment"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ec2.resource_providers.aws_ec2_transitgatewayattachment import (
            EC2TransitGatewayAttachmentProvider,
        )

        self.factory = EC2TransitGatewayAttachmentProvider
