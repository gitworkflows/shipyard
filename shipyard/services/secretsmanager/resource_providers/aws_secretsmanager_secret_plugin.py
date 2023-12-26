from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SecretsManagerSecretProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SecretsManager::Secret"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.secretsmanager.resource_providers.aws_secretsmanager_secret import (
            SecretsManagerSecretProvider,
        )

        self.factory = SecretsManagerSecretProvider
