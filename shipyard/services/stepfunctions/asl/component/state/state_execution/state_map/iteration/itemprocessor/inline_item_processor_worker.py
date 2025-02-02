import copy
import logging
from typing import Final, Optional

from shipyard.services.stepfunctions.asl.component.state.state_execution.state_map.item_selector import (
    ItemSelector,
)
from shipyard.services.stepfunctions.asl.component.state.state_execution.state_map.iteration.iteration_worker import (
    IterationWorker,
)
from shipyard.services.stepfunctions.asl.component.state.state_execution.state_map.iteration.job import (
    JobPool,
)
from shipyard.services.stepfunctions.asl.eval.environment import Environment

LOG = logging.getLogger(__name__)


class InlineItemProcessorWorker(IterationWorker):
    _item_selector: Final[Optional[ItemSelector]]

    def __init__(
        self,
        work_name: str,
        job_pool: JobPool,
        env: Environment,
        item_selector: Optional[ItemSelector],
    ):
        super().__init__(work_name=work_name, job_pool=job_pool, env=env)
        self._item_selector = item_selector

    def _eval_input(self, env_frame: Environment) -> None:
        if self._item_selector:
            map_state_input = self._env.stack[-1]
            env_frame.inp = copy.deepcopy(map_state_input)
            env_frame.stack.append(env_frame.inp)
            self._item_selector.eval(env_frame)
            env_frame.inp = env_frame.stack.pop()
            env_frame.stack.append(env_frame.inp)
