import unittest
from . grammar import Grammar, NonTerminalSymbol

from lexer.tokens import (
    StarToken, PlusToken, IdentifierToken,
    RoundBracketOpenToken, RoundBracketCloseToken
)

class TestFirstAndFollow(unittest.TestCase):
    def testGrammar1(self):
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")

        rules = {
            A : [[B, StarToken]],
            B : [[PlusToken]]
        }

        g = Grammar(A, rules)
        
        self.assertEqual(g.first(A), {PlusToken})
        self.assertEqual(g.first(B), {PlusToken})
        self.assertEqual(g.follow(A), {"$"})
        self.assertEqual(g.follow(B), {StarToken})

    def testGrammar2(self):
        A = NonTerminalSymbol("A")

        rules = {
            A : [[PlusToken, A], []]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.first(A), {PlusToken, None})
        self.assertEqual(g.follow(A), {"$"})

    def testGrammar3(self):
        E = NonTerminalSymbol("E")
        E2 = NonTerminalSymbol("E'")
        T = NonTerminalSymbol("T")
        T2 = NonTerminalSymbol("T'")
        F = NonTerminalSymbol("F")

        rules = {
            E : [[T, E2]],
            E2 : [[PlusToken, T, E2], []],
            T : [[F, T2]],
            T2 : [[StarToken, F, T2], []],
            F : [[RoundBracketOpenToken, E, RoundBracketCloseToken], [IdentifierToken]]
        }

        g = Grammar(E, rules)

        self.assertEqual(g.first(E), {RoundBracketOpenToken, IdentifierToken})
        self.assertEqual(g.first(E2), {PlusToken, None})
        self.assertEqual(g.first(T), {RoundBracketOpenToken, IdentifierToken})
        self.assertEqual(g.first(T2), {StarToken, None})
        self.assertEqual(g.first(F), {RoundBracketOpenToken, IdentifierToken})

        self.assertEqual(g.follow(E), {"$", RoundBracketCloseToken})
        self.assertEqual(g.follow(E2), {"$", RoundBracketCloseToken})
        self.assertEqual(g.follow(T), {PlusToken, "$", RoundBracketCloseToken})
        self.assertEqual(g.follow(T2), {PlusToken, "$", RoundBracketCloseToken})
        self.assertEqual(g.follow(F), {StarToken, PlusToken, "$", RoundBracketCloseToken})

    def testGrammar4(self):
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")

        rules = {
            A : [[PlusToken, B]],
            B : [[A], []]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.first(A), {PlusToken})
        self.assertEqual(g.first(B), {None, PlusToken})
        self.assertEqual(g.follow(A), {"$"})
        self.assertEqual(g.follow(B), {"$"})

class TestGetTerminals(unittest.TestCase):
    def testSimple(self):
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")

        rules = {
            A : [[StarToken, B, PlusToken], [PlusToken]],
            B : [[RoundBracketOpenToken]]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.getTerminals(), {StarToken, PlusToken, RoundBracketOpenToken})