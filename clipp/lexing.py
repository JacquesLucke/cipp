from lexer import Lexer

from . tokens import (
    IdentifierToken, IntegerToken, CommentToken,
    WhitespaceToken, SingleCharToken
)

clippLexer = Lexer(
    [IdentifierToken, IntegerToken, CommentToken, 
     SingleCharToken, WhitespaceToken], 
    ignoredTokenTypes = [WhitespaceToken, CommentToken]
)