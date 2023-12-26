from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class SchedulerScheduleGroupProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::Scheduler::ScheduleGroup"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.scheduler.resource_providers.aws_scheduler_schedulegroup import (
            SchedulerScheduleGroupProvider,
        )

        self.factory = SchedulerScheduleGroupProvider
