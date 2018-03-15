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

Expr = NonTerminalSymbol("Expr")
Expr2 = NonTerminalSymbol("Expr'")
Term = NonTerminalSymbol("Term")
Term2 = NonTerminalSymbol("Term'")
Factor = NonTerminalSymbol("Factor")

rules = {
    Expr : [
        [Term, Expr2]
    ],
    Expr2 : [
        [PlusToken, Expr],
        [MinusToken, Expr],
        []
    ],
    Term : [
        [Factor, Term2]
    ],
    Term2 : [
        [StarToken, Term],
        [SlashToken, Term],
        []
    ],
    Factor : [
        [IntegerToken],
        [IdentifierToken],
        [MinusToken, Factor],
        [RoundBracketOpenToken, Expr, RoundBracketCloseToken]
    ],
}

grammar = Grammar(Expr, rules)

tree = checkIfStringMatchesGrammar("4+5*(1 -4)+a", lexer, grammar)
print(tree.toTreeString())

class ExprAST:
    def __new__(cls, root):
        term, expr2 = root.children
        if expr2.production == rules[Expr2][0]:
            return PlusNode(term, expr2.children[1])
        elif expr2.production == rules[Expr2][1]:
            return MinusNode(term, expr2.children[1])
        elif expr2.production == rules[Expr2][2]:
            return TermAST(term)

class TermAST:
    def __new__(cls, root):
        factor, term2 = root.children
        if term2.production == rules[Term2][0]:
            return MulNode(factor, term2.children[1])
        elif term2.production == rules[Term2][1]:
            return DivNode(factor, term2.children[1])
        elif term2.production == rules[Term2][2]:
            return FactorAST(factor)

class FactorAST:
    def __new__(cls, root):
        if root.production == rules[Factor][0]:
            return IntegerNode(root.children[0][0])
        elif root.production == rules[Factor][1]:
            return IdentifierNode(root.children[0][0])
        elif root.production == rules[Factor][2]:
            return NegateNode(root.children[1])
        elif root.production == rules[Factor][3]:
            return ExprAST(root.children[1])

class ASTNode:
    def toTreeString(self):
        return "\n".join(self.iterTreeStringLines())

    def iterTreeStringLines(self):
        yield self.getName()
        for child in self.children:
            for line in child.iterTreeStringLines():
                yield f"  |{line}" 

    def getName(self):
        return type(self).__name__


class PlusNode(ASTNode):
    def __init__(self, term, expr):
        self.a = TermAST(term)
        self.b = ExprAST(expr)
        self.children = [self.a, self.b]

class MinusNode(ASTNode):
    def __init__(self, term, expr):
        self.a = TermAST(term)
        self.b = ExprAST(expr)
        self.children = [self.a, self.b]

class MulNode(ASTNode):
    def __init__(self, factor, term):
        self.a = FactorAST(factor)
        self.b = TermAST(term)
        self.children = [self.a, self.b]

class DivNode(ASTNode):
    def __init__(self, factor, term):
        self.a = FactorAST(factor)
        self.b = TermAST(term)
        self.children = [self.a, self.b]

class IntegerNode(ASTNode):
    def __init__(self, token):
        self.value = token.number
        self.children = []

    def getName(self):
        return str(self.value)

class IdentifierNode(ASTNode):
    def __init__(self, token):
        self.value = token.content
        self.children = []

    def getName(self):
        return self.value

class NegateNode(ASTNode):
    def __init__(self, factor):
        self.a = FactorAST(factor)
        self.children = [self.a]

parsedExpression = ExprAST(tree)
print(parsedExpression.toTreeString())