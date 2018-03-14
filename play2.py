from LL1parser.grammar import Grammar, NonTerminalSymbol
from LL1parser.parser import checkIfStringMatchesGrammar
from lexer.lexer import Lexer
from lexer.tokens import (
    createTokenTypeFromLetter,
    EqualToken, IdentifierToken, IntegerToken, 
    PlusToken, MinusToken, StarToken, SlashToken,
    RoundBracketOpenToken, RoundBracketCloseToken,
    WhitespaceToken, IntegerToken
)

lexer = Lexer(
    [PlusToken, MinusToken, StarToken, SlashToken, WhitespaceToken,
     IdentifierToken, RoundBracketOpenToken, RoundBracketCloseToken,
     IntegerToken],
    ignoredTokenTypes = [WhitespaceToken]
)

expr = NonTerminalSymbol("Expr")
expr2 = NonTerminalSymbol("Expr'")
term = NonTerminalSymbol("Term")
term2 = NonTerminalSymbol("Term'")
factor = NonTerminalSymbol("Factor")

rules = {
    expr : [
        [term, expr2]
    ],
    expr2 : [
        [PlusToken, expr],
        [MinusToken, expr],
        []
    ],
    term : [
        [factor, term2]
    ],
    term2 : [
        [StarToken, term],
        [SlashToken, term],
        []
    ],
    factor : [
        [IntegerToken],
        [IdentifierToken],
        [MinusToken, factor],
        [RoundBracketOpenToken, expr, RoundBracketCloseToken]
    ],
}

grammar = Grammar(expr, rules)

checkIfStringMatchesGrammar("(a + b) * c", lexer, grammar)