from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class DynamoDBTableProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::DynamoDB::Table"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.dynamodb.resource_providers.aws_dynamodb_table import (
            DynamoDBTableProvider,
        )

        self.factory = DynamoDBTableProvider
