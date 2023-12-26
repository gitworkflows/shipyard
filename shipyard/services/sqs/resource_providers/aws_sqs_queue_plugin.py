from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SQSQueueProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SQS::Queue"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.sqs.resource_providers.aws_sqs_queue import SQSQueueProvider

        self.factory = SQSQueueProvider
