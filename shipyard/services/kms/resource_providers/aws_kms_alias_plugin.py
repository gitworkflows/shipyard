from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class KMSAliasProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::KMS::Alias"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.kms.resource_providers.aws_kms_alias import KMSAliasProvider

        self.factory = KMSAliasProvider
