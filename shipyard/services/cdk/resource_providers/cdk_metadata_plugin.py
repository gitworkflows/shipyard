from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LambdaAliasProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::CDK::Metadata"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.cdk.resource_providers.cdk_metadata import CDKMetadataProvider

        self.factory = CDKMetadataProvider
