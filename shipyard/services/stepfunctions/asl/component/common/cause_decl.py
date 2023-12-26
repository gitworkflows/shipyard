from typing import Final

from shipyard.services.stepfunctions.asl.component.component import Component


class CauseDecl(Component):
    def __init__(self, cause: str):
        self.cause: Final[str] = cause
