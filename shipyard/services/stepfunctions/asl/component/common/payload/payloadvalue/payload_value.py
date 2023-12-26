import abc

from shipyard.services.stepfunctions.asl.component.eval_component import EvalComponent


class PayloadValue(EvalComponent, abc.ABC):
    ...
