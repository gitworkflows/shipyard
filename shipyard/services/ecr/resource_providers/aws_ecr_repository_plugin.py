from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class ECRRepositoryProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::ECR::Repository"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ecr.resource_providers.aws_ecr_repository import (
            ECRRepositoryProvider,
        )

        self.factory = ECRRepositoryProvider
