from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SecretsManagerRotationScheduleProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SecretsManager::RotationSchedule"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.secretsmanager.resource_providers.aws_secretsmanager_rotationschedule import (
            SecretsManagerRotationScheduleProvider,
        )

        self.factory = SecretsManagerRotationScheduleProvider
