from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class LogsLogStreamProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Logs::LogStream"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.logs.resource_providers.aws_logs_logstream import (
            LogsLogStreamProvider,
        )

        self.factory = LogsLogStreamProvider
