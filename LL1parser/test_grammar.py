import unittest
from . token_stream import EOFToken
from . grammar import Grammar, NonTerminalSymbol

from lexer.tokens import (
    StarToken, PlusToken, IdentifierToken,
    RoundBracketOpenToken, RoundBracketCloseToken,
    createTokenTypeFromLetter
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
        self.assertEqual(g.follow(A), {EOFToken})
        self.assertEqual(g.follow(B), {StarToken})

    def testGrammar2(self):
        A = NonTerminalSymbol("A")

        rules = {
            A : [[PlusToken, A], []]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.first(A), {PlusToken, None})
        self.assertEqual(g.follow(A), {EOFToken})

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

        self.assertEqual(g.follow(E), {EOFToken, RoundBracketCloseToken})
        self.assertEqual(g.follow(E2), {EOFToken, RoundBracketCloseToken})
        self.assertEqual(g.follow(T), {PlusToken, EOFToken, RoundBracketCloseToken})
        self.assertEqual(g.follow(T2), {PlusToken, EOFToken, RoundBracketCloseToken})
        self.assertEqual(g.follow(F), {StarToken, PlusToken, EOFToken, RoundBracketCloseToken})

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
        self.assertEqual(g.follow(A), {EOFToken})
        self.assertEqual(g.follow(B), {EOFToken})
    
    def testGrammar5(self):
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")
        C = NonTerminalSymbol("C")

        rules = {
            A : [[B, C]],
            B : [[]],
            C : [[PlusToken]]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.first(A), {PlusToken})
        self.assertEqual(g.first(B), {None})
        self.assertEqual(g.first(C), {PlusToken})
        self.assertEqual(g.follow(A), {EOFToken})
        self.assertEqual(g.follow(B), {PlusToken})
        self.assertEqual(g.follow(C), {EOFToken})

        self.assertEqual(g.first([B, C]), {PlusToken})

    def testGrammar6(self):
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")
        C = NonTerminalSymbol("C")
        D = NonTerminalSymbol("D")

        rules = {
            A : [[B]],
            B : [[]],
            C : [[PlusToken]]
        }

        g = Grammar(A, rules)

        self.assertEqual(g.first(A), {None})
        self.assertEqual(g.first(B), {None})
        self.assertEqual(g.first([A, C]), {PlusToken})

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

class TestParsingTableCreation(unittest.TestCase):
    def testSimple(self):
        # https://www.hsg-kl.de/faecher/inf/compiler/parser/LL1/index.php

        S = NonTerminalSymbol("S")
        A = NonTerminalSymbol("A")
        B = NonTerminalSymbol("B")
        C = NonTerminalSymbol("C")

        a = createTokenTypeFromLetter("a")
        b = createTokenTypeFromLetter("b")
        c = createTokenTypeFromLetter("c")

        rules = {
            S : [[A, B, c, C]],
            A : [[a, A], []],
            B : [[b, b, B], []],
            C : [[B, A]]
        }

        grammar = Grammar(S, rules)
        table = grammar.createParsingTable()

        self.assertEqual(table[(S, a)], [A, B, c, C])
        self.assertEqual(table[(S, b)], [A, B, c, C])
        self.assertEqual(table[(S, c)], [A, B, c, C])

        self.assertEqual(table[(A, a)], [a, A])
        self.assertEqual(table[(A, b)], [])
        self.assertEqual(table[(A, c)], [])
        self.assertEqual(table[(A, EOFToken)], [])

        self.assertEqual(table[(B, a)], [])
        self.assertEqual(table[(B, b)], [b, b, B])
        self.assertEqual(table[(B, c)], [])
        self.assertEqual(table[(B, EOFToken)], [])

        self.assertEqual(table[(C, a)], [B, A])
        self.assertEqual(table[(C, b)], [B, A])
        self.assertEqual(table[(C, EOFToken)], [B, A])

        with self.assertRaises(KeyError):
            table[(S, EOFToken)]
        with self.assertRaises(KeyError):
            table[(C, c)]