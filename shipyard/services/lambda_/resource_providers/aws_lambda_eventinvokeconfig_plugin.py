from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LambdaEventInvokeConfigProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Lambda::EventInvokeConfig"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.lambda_.resource_providers.aws_lambda_eventinvokeconfig import (
            LambdaEventInvokeConfigProvider,
        )

        self.factory = LambdaEventInvokeConfigProvider
