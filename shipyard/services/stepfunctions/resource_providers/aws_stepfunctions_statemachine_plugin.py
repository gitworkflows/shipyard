from typing import Optional, Type

from shipyard.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class StepFunctionsStateMachineProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::StepFunctions::StateMachine"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from shipyard.services.stepfunctions.resource_providers.aws_stepfunctions_statemachine import (
            StepFunctionsStateMachineProvider,
        )

        self.factory = StepFunctionsStateMachineProvider
