from typing import Final

from shipyard.services.stepfunctions.asl.component.common.payload.payloadvalue.payloadtmpl.payload_tmpl import (
    PayloadTmpl,
)
from shipyard.services.stepfunctions.asl.component.eval_component import EvalComponent
from shipyard.services.stepfunctions.asl.eval.environment import Environment


class Parameters(EvalComponent):
    def __init__(self, payload_tmpl: PayloadTmpl):
        self.payload_tmpl: Final[PayloadTmpl] = payload_tmpl

    def _eval_body(self, env: Environment) -> None:
        self.payload_tmpl.eval(env=env)
