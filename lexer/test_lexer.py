import unittest
from . lexer import Lexer
from . tokens import (
    RoundBracketOpenToken, RoundBracketCloseToken, CommaToken,
    WhitespaceToken, IdentifierToken, IntegerToken
)

bracketLexer = Lexer(
    [RoundBracketOpenToken, RoundBracketCloseToken, WhitespaceToken],
    ignoredTokenTypes = [WhitespaceToken]
)

nameLexer = Lexer(
    [IdentifierToken, WhitespaceToken],
    ignoredTokenTypes = [WhitespaceToken]
)

integerLexer = Lexer(
    [IntegerToken, WhitespaceToken],
    ignoredTokenTypes = [WhitespaceToken]
)

integerIdentifierLexer = Lexer(
    [IntegerToken, IdentifierToken, WhitespaceToken],
    ignoredTokenTypes = [WhitespaceToken]
)

class TestLexer(unittest.TestCase):
    def testBracketLexer(self):
        self.assertLexerResult(" (( )(  ) ", bracketLexer,
            '''
            <RoundBracketOpenToken>
            <RoundBracketOpenToken>
            <RoundBracketCloseToken>
            <RoundBracketOpenToken>
            <RoundBracketCloseToken>
            ''')

    def testUnknownToken(self):
        with self.assertRaises(Exception):
            list(bracketLexer.tokenize("( )(,)"))

    def testIdentifierToken(self):
        tokens = self.assertLexerResult("hello world3  te4st ", nameLexer,
            '''
            <IdentifierToken:hello>
            <IdentifierToken:world3>
            <IdentifierToken:te4st>
            ''')
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].value, "hello")
        self.assertEqual(tokens[1].value, "world3")
        self.assertEqual(tokens[2].value, "te4st")

    def testIntegerToken(self):
        tokens = self.assertLexerResult(" 32 42 54  ", integerLexer,
            '''
            <IntegerToken:32>
            <IntegerToken:42>
            <IntegerToken:54>
            ''')
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].value, 32)
        self.assertEqual(tokens[1].value, 42)
        self.assertEqual(tokens[2].value, 54)

    def testIntegerAndName(self):
        self.assertLexerResult(" hello 32 world 12 tes_t10 _32", integerIdentifierLexer,
            '''
            <IdentifierToken:hello>
            <IntegerToken:32>
            <IdentifierToken:world>
            <IntegerToken:12>
            <IdentifierToken:tes_t10>
            <IdentifierToken:_32>
            ''')

    def testInvalidInteger(self):
        with self.assertRaises(Exception):
            list(Lexer(integerIdentifierLexer, "13q"))

    def assertLexerResult(self, string, lexer, expected):
        tokens = list(lexer.tokenize(string))
        result = "".join(map(repr, tokens)).replace(" ", "")
        expected = expected.replace(" ", "").replace("\n", "")
        self.assertEqual(expected, result)
        return tokens