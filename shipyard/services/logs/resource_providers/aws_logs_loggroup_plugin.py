from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LogsLogGroupProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Logs::LogGroup"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.logs.resource_providers.aws_logs_loggroup import (
            LogsLogGroupProvider,
        )

        self.factory = LogsLogGroupProvider
