from typing import Final

from shipyard.services.stepfunctions.asl.component.eval_component import EvalComponent
from shipyard.services.stepfunctions.asl.eval.environment import Environment
from shipyard.services.stepfunctions.asl.utils.json_path import JSONPathUtils


class NoSuchVariable:
    def __init__(self, path: str):
        self.path: Final[str] = path


class Variable(EvalComponent):
    def __init__(self, value: str):
        self.value: Final[str] = value

    def _eval_body(self, env: Environment) -> None:
        try:
            inp = env.stack[-1]
            value = JSONPathUtils.extract_json(self.value, inp)
        except Exception as ex:
            value = NoSuchVariable(f"{self.value}, {ex}")
        env.stack.append(value)
