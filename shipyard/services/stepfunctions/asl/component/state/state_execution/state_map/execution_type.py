from enum import Enum

from shipyard.services.stepfunctions.asl.antlr.runtime.ASLLexer import ASLLexer


class ExecutionType(Enum):
    Standard = ASLLexer.STANDARD
