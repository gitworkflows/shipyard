from __future__ import annotations

import json
from typing import Final

from shipyard.services.stepfunctions.asl.component.eval_component import EvalComponent
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.comparison_operator_type import (
    ComparisonOperatorType,
)
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.factory import (
    OperatorFactory,
)
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.operator import (
    Operator,
)
from shipyard.services.stepfunctions.asl.eval.environment import Environment


class ComparisonFunc(EvalComponent):
    def __init__(self, operator: ComparisonOperatorType, value: json):
        self.operator_type: Final[ComparisonOperatorType] = operator
        self.value: json = value

    def _eval_body(self, env: Environment) -> None:
        value = self.value
        operator: Operator = OperatorFactory.get(self.operator_type)
        operator.eval(env=env, value=value)

    @staticmethod
    def _string_equals(env: Environment, value: json) -> None:
        val = env.stack.pop()
        res = str(val) == value
        env.stack.append(res)
