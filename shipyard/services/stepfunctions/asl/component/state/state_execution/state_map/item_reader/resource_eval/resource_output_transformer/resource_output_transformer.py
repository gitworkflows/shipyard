import abc

from shipyard.services.stepfunctions.asl.component.eval_component import EvalComponent


class ResourceOutputTransformer(EvalComponent, abc.ABC):
    ...
