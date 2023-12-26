from typing import Any

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


class StatesFunctionArray(StatesFunction):
    def __init__(self, arg_list: FunctionArgumentList):
        super().__init__(
            states_name=StatesFunctionName(function_type=StatesFunctionNameType.Array),
            arg_list=arg_list,
        )

    def _eval_body(self, env: Environment) -> None:
        self.arg_list.eval(env=env)
        values: list[Any] = list()
        for _ in range(self.arg_list.size):
            values.append(env.stack.pop())
        values.reverse()
        env.stack.append(values)
