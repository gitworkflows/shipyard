from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.comparison_operator_type import (
    ComparisonOperatorType,
)
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.implementations.boolean_equals import *  # noqa
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.implementations.is_operator import *  # noqa
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.implementations.numeric import *  # noqa
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.implementations.string_operators import *  # noqa
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.implementations.timestamp_operators import *  # noqa
from shipyard.services.stepfunctions.asl.component.state.state_choice.comparison.operator.operator import (
    Operator,
)


class OperatorFactory:
    @staticmethod
    def get(typ: ComparisonOperatorType) -> Operator:
        op = Operator.get((str(typ)), raise_if_missing=False)
        if op is None:
            raise NotImplementedError(f"{typ} is not supported.")
        return op
