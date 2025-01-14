import abc
from typing import Any, Final

from shipyard.services.stepfunctions.asl.component.common.payload.payloadvalue.payload_value import (
    PayloadValue,
)
from shipyard.services.stepfunctions.asl.eval.environment import Environment


class PayloadBinding(PayloadValue, abc.ABC):
    def __init__(self, field: str):
        self.field: Final[str] = field

    @abc.abstractmethod
    def _eval_val(self, env: Environment) -> Any:
        ...

    def _eval_body(self, env: Environment) -> None:
        cnt: dict = env.stack.pop()
        val = self._eval_val(env=env)
        cnt[self.field] = val
        env.stack.append(cnt)
