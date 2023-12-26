from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class DynamoDBGlobalTableProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::DynamoDB::GlobalTable"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.dynamodb.resource_providers.aws_dynamodb_globaltable import (
            DynamoDBGlobalTableProvider,
        )

        self.factory = DynamoDBGlobalTableProvider
