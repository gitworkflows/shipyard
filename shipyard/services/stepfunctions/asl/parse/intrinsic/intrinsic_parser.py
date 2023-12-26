import abc

from antlr4 import CommonTokenStream, InputStream

from shipyard.services.stepfunctions.asl.antlr.runtime.ASLIntrinsicLexer import ASLIntrinsicLexer
from shipyard.services.stepfunctions.asl.antlr.runtime.ASLIntrinsicParser import (
    ASLIntrinsicParser,
)
from shipyard.services.stepfunctions.asl.component.intrinsic.function.function import Function
from shipyard.services.stepfunctions.asl.parse.intrinsic.preprocessor import Preprocessor


class IntrinsicParser(abc.ABC):
    @staticmethod
    def parse(src: str) -> Function:
        input_stream = InputStream(src)
        lexer = ASLIntrinsicLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ASLIntrinsicParser(stream)
        tree = parser.func_decl()
        preprocessor = Preprocessor()
        function: Function = preprocessor.visit(tree)
        return function
