from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class ApiGatewayRequestValidatorProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::ApiGateway::RequestValidator"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.apigateway.resource_providers.aws_apigateway_requestvalidator import (
            ApiGatewayRequestValidatorProvider,
        )

        self.factory = ApiGatewayRequestValidatorProvider
