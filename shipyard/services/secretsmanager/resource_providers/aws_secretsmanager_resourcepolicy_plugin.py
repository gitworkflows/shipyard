from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SecretsManagerResourcePolicyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SecretsManager::ResourcePolicy"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.secretsmanager.resource_providers.aws_secretsmanager_resourcepolicy import (
            SecretsManagerResourcePolicyProvider,
        )

        self.factory = SecretsManagerResourcePolicyProvider
