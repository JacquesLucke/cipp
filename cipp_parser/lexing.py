from lexer import Lexer

from . tokens import (
    IdentifierToken, IntegerToken, CommentToken,
    WhitespaceToken, SingleCharToken
)

cippLexer = Lexer(
    [IdentifierToken, IntegerToken, CommentToken, 
     SingleCharToken, WhitespaceToken], 
    ignoredTokens = [WhitespaceToken, CommentToken]
)