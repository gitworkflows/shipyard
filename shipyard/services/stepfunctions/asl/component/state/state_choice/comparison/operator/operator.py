import abc
from typing import Any

from shipyard.services.stepfunctions.asl.eval.environment import Environment
from shipyard.utils.objects import SubtypesInstanceManager


class Operator(abc.ABC, SubtypesInstanceManager):
    @staticmethod
    @abc.abstractmethod
    def eval(env: Environment, value: Any) -> None:
        pass
