from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LambdaUrlProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Lambda::Url"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.lambda_.resource_providers.aws_lambda_url import LambdaUrlProvider

        self.factory = LambdaUrlProvider
