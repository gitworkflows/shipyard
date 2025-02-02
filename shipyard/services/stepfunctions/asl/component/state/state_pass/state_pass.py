from typing import Optional

from shipyard.aws.api.stepfunctions import (
    HistoryEventExecutionDataDetails,
    HistoryEventType,
    StateEnteredEventDetails,
    StateExitedEventDetails,
)
from shipyard.services.stepfunctions.asl.component.common.parameters import Parameters
from shipyard.services.stepfunctions.asl.component.common.path.result_path import ResultPath
from shipyard.services.stepfunctions.asl.component.state.state import CommonStateField
from shipyard.services.stepfunctions.asl.component.state.state_pass.result import Result
from shipyard.services.stepfunctions.asl.component.state.state_props import StateProps
from shipyard.services.stepfunctions.asl.eval.environment import Environment
from shipyard.services.stepfunctions.asl.utils.encoding import to_json_str


class StatePass(CommonStateField):
    def __init__(self):
        super(StatePass, self).__init__(
            state_entered_event_type=HistoryEventType.PassStateEntered,
            state_exited_event_type=HistoryEventType.PassStateExited,
        )

        # Result (Optional)
        # Refers to the output of a virtual state_task that is passed on to the next state. If you include the ResultPath
        # field in your state machine definition, Result is placed as specified by ResultPath and passed on to the
        self.result: Optional[Result] = None

        # ResultPath (Optional)
        # Specifies where to place the output (relative to the input) of the virtual state_task specified in Result. The input
        # is further filtered as specified by the OutputPath field (if present) before being used as the state's output.
        self.result_path: Optional[ResultPath] = None

        # Parameters (Optional)
        # Creates a collection of key-value pairs that will be passed as input. You can specify Parameters as a static
        # value or select from the input using a path.
        self.parameters: Optional[Parameters] = None

    def from_state_props(self, state_props: StateProps) -> None:
        super(StatePass, self).from_state_props(state_props)
        self.result = state_props.get(Result)
        self.result_path = state_props.get(ResultPath) or ResultPath(
            result_path_src=ResultPath.DEFAULT_PATH
        )
        self.parameters = state_props.get(Parameters)

    def _get_state_entered_event_details(self, env: Environment) -> StateEnteredEventDetails:
        return StateEnteredEventDetails(
            name=self.name,
            input=to_json_str(env.inp, separators=(",", ":")),
            inputDetails=HistoryEventExecutionDataDetails(
                truncated=False  # Always False for api calls.
            ),
        )

    def _get_state_exited_event_details(self, env: Environment) -> StateExitedEventDetails:
        return StateExitedEventDetails(
            name=self.name,
            output=to_json_str(env.inp, separators=(",", ":")),
            outputDetails=HistoryEventExecutionDataDetails(
                truncated=False  # Always False for api calls.
            ),
        )

    def _eval_state(self, env: Environment) -> None:
        if self.parameters:
            self.parameters.eval(env=env)

        if self.result:
            env.stack.append(self.result.result_obj)

        if self.result_path:
            self.result_path.eval(env)
