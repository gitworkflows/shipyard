from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SSMMaintenanceWindowTargetProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::SSM::MaintenanceWindowTarget"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.ssm.resource_providers.aws_ssm_maintenancewindowtarget import (
            SSMMaintenanceWindowTargetProvider,
        )

        self.factory = SSMMaintenanceWindowTargetProvider
