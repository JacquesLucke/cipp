import unittest
from lexer import Lexer
from . lexing import cippLexer
from . tokens import (
    CommentToken, SingleCharToken, WhitespaceToken, 
    IdentifierToken, IntegerToken,
    createSingleCharToken
)

class TestTokens(unittest.TestCase):
    def testWhitespaceToken(self):
        PlusToken = createSingleCharToken("+")
        lexer = Lexer([PlusToken, WhitespaceToken])

        tokens = lexer.tokenize("+   ++    +  ")
        self.assertIsInstance(tokens[0], PlusToken)
        self.assertIsInstance(tokens[1], WhitespaceToken)
        self.assertIsInstance(tokens[2], PlusToken)
        self.assertIsInstance(tokens[3], PlusToken)
        self.assertIsInstance(tokens[4], WhitespaceToken)
        self.assertIsInstance(tokens[5], PlusToken)
        self.assertIsInstance(tokens[6], WhitespaceToken)

    def testCommentToken(self):
        PlusToken = createSingleCharToken("+")
        lexer = Lexer([PlusToken, WhitespaceToken, CommentToken])

        tokens = lexer.tokenize("+  # my comment \n  +  # comment 2 # still\n  #test")
        self.assertIsInstance(tokens[0], PlusToken)
        self.assertIsInstance(tokens[1], WhitespaceToken)
        self.assertIsInstance(tokens[2], CommentToken)
        self.assertEqual(tokens[2].value, " my comment ")
        self.assertIsInstance(tokens[3], WhitespaceToken)
        self.assertIsInstance(tokens[4], PlusToken)
        self.assertIsInstance(tokens[5], WhitespaceToken)
        self.assertIsInstance(tokens[6], CommentToken)
        self.assertEqual(tokens[6].value, " comment 2 # still")
        self.assertIsInstance(tokens[7], WhitespaceToken)
        self.assertIsInstance(tokens[8], CommentToken)
        self.assertEqual(tokens[8].value, "test")

    def testIdentifierToken(self):
        lexer = Lexer([IdentifierToken, WhitespaceToken], ignoredTokens = [WhitespaceToken])

        tokens = lexer.tokenize("who where3 whe6N why_ WH_at _which _ho4_w_ _")
        self.assertEqual(tokens[0].value, "who")
        self.assertEqual(tokens[1].value, "where3")
        self.assertEqual(tokens[2].value, "whe6N")
        self.assertEqual(tokens[3].value, "why_")
        self.assertEqual(tokens[4].value, "WH_at")
        self.assertEqual(tokens[5].value, "_which")
        self.assertEqual(tokens[6].value, "_ho4_w_")
        self.assertEqual(tokens[7].value, "_")

    def testIdentifierDoesNotStartWithDigit(self):
        lexer = Lexer([IdentifierToken])
        with self.assertRaises(Exception):
            lexer.tokenize("4")
        with self.assertRaises(Exception):
            lexer.tokenize("32a")

    def testIntegerToken(self):
        lexer = Lexer([IntegerToken, WhitespaceToken], ignoredTokens = [WhitespaceToken])

        tokens = lexer.tokenize("34 12 546")
        self.assertEqual(tokens[0].value, 34)
        self.assertEqual(tokens[1].value, 12)
        self.assertEqual(tokens[2].value, 546)

class TestCippLexer(unittest.TestCase):
    def testFunctionHead(self):
        tokens = cippLexer.tokenize("def int @test(int a, int b)")
        self.assertIdentifierToken(tokens[0], "def")
        self.assertIdentifierToken(tokens[1], "int")
        self.assertSingleCharToken(tokens[2], "@")
        self.assertIdentifierToken(tokens[3], "test")
        self.assertSingleCharToken(tokens[4], "(")
        self.assertIdentifierToken(tokens[5], "int")
        self.assertIdentifierToken(tokens[6], "a")
        self.assertSingleCharToken(tokens[7], ",")
        self.assertIdentifierToken(tokens[8], "int")
        self.assertIdentifierToken(tokens[9], "b")
        self.assertSingleCharToken(tokens[10], ")")

    def assertIdentifierToken(self, token, value):
        self.assertIsInstance(token, IdentifierToken)
        self.assertEqual(token.value, value)

    def assertSingleCharToken(self, token, char):
        self.assertIsInstance(token, SingleCharToken)
        self.assertEqual(token.value, char)