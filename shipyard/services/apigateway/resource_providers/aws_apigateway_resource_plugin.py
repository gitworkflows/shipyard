from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class ApiGatewayResourceProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::ApiGateway::Resource"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.apigateway.resource_providers.aws_apigateway_resource import (
            ApiGatewayResourceProvider,
        )

        self.factory = ApiGatewayResourceProvider
