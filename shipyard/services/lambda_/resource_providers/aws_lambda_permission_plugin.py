from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LambdaPermissionProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Lambda::Permission"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.lambda_.resource_providers.aws_lambda_permission import (
            LambdaPermissionProvider,
        )

        self.factory = LambdaPermissionProvider
