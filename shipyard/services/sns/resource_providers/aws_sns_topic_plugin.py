from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SNSTopicProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SNS::Topic"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.sns.resource_providers.aws_sns_topic import SNSTopicProvider

        self.factory = SNSTopicProvider
