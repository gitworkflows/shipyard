from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class ApiGatewayDeploymentProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::ApiGateway::Deployment"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.apigateway.resource_providers.aws_apigateway_deployment import (
            ApiGatewayDeploymentProvider,
        )

        self.factory = ApiGatewayDeploymentProvider
