from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class KMSKeyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::KMS::Key"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.kms.resource_providers.aws_kms_key import KMSKeyProvider

        self.factory = KMSKeyProvider
