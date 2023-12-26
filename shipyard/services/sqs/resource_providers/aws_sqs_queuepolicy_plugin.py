from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SQSQueuePolicyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SQS::QueuePolicy"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.sqs.resource_providers.aws_sqs_queuepolicy import (
            SQSQueuePolicyProvider,
        )

        self.factory = SQSQueuePolicyProvider
