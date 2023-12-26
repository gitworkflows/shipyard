import json

from shipyard.services.stepfunctions.asl.component.intrinsic.argument.function_argument_list import (
    FunctionArgumentList,
)
from shipyard.services.stepfunctions.asl.component.intrinsic.function.statesfunction.states_function import (
    StatesFunction,
)
from shipyard.services.stepfunctions.asl.component.intrinsic.functionname.state_function_name_types import (
    StatesFunctionNameType,
)
from shipyard.services.stepfunctions.asl.component.intrinsic.functionname.states_function_name import (
    StatesFunctionName,
)
from shipyard.services.stepfunctions.asl.eval.environment import Environment


class StatesFunctionStringToJson(StatesFunction):
    def __init__(self, arg_list: FunctionArgumentList):
        super().__init__(
            states_name=StatesFunctionName(function_type=StatesFunctionNameType.StringToJson),
            arg_list=arg_list,
        )
        if arg_list.size != 1:
            raise ValueError(
                f"Expected 1 argument for function type '{type(self)}', but got: '{arg_list}'."
            )

    def _eval_body(self, env: Environment) -> None:
        self.arg_list.eval(env=env)
        string_json: str = env.stack.pop()
        json_obj: json = json.loads(string_json)
        env.stack.append(json_obj)
