import unittest
from . import parser
tokenize = parser.stringToTokenStream

class TestSelectStatementParser(unittest.TestCase):
    def testBlock(self):
        stmt = self.parseStatement("{a=b;c=d;}")
        self.assertIsInstance(stmt, parser.BlockStmtAST)

    def testReturn(self):
        stmt = self.parseStatement("return 3;")
        self.assertIsInstance(stmt, parser.ReturnStmtAST)

    def testLet(self):
        stmt = self.parseStatement("let int variable = 42;")
        self.assertIsInstance(stmt, parser.LetStmtAST)

    def testWhile(self):
        stmt = self.parseStatement("while (1 < 2) {}")
        self.assertIsInstance(stmt, parser.WhileStmtAST)

    def testIf(self):
        stmt = self.parseStatement("if (1 < 2) {}")
        self.assertIsInstance(stmt, parser.IfStmtAST)

    def testIfElse(self):
        stmt = self.parseStatement("if (1) {} else {}")
        self.assertIsInstance(stmt, parser.IfElseStmtAST)

    def parseStatement(self, code):
        tokens = tokenize(code)
        return parser.parseStatement(tokens)

class TestParseFunctionCall(unittest.TestCase):
    def testNormal(self):
        ast = self.parseFunctionCall("@hello(3+4, 2*a)")
        self.assertEqual(ast.functionName, "hello")
        self.assertEqual(len(ast.arguments), 2)

    def testMissingAt(self):
        with self.assertRaises(Exception):
            self.parseFunctionCall("hello(1, 1)")

    def testNoArguments(self):
        ast = self.parseFunctionCall("@test()")
        self.assertEqual(ast.functionName, "test")
        self.assertEqual(len(ast.arguments), 0)  

    def testForgottenComma(self):
        with self.assertRaises(Exception):
            self.parseFunctionCall("@test(2 3)")    

    def parseFunctionCall(self, code):
        tokens = tokenize(code)
        ast = parser.parseFunctionCall(tokens)
        self.assertIsInstance(ast, parser.FunctionCallAST)
        return ast

class TestParseExpression(unittest.TestCase):
    def testSimpleAdd(self):
        ast = self.parseExpression("3 + a")
        self.assertIsInstance(ast, parser.AddSubExprAST)
        self.assertEqual(ast.terms[0].expr.value, 3)
        self.assertEqual(ast.terms[1].expr.name, "a")

    def testAddAndSub(self):
        ast = self.parseExpression("1 + a - 4 - 3 + test")
        self.assertIsInstance(ast, parser.AddSubExprAST)
        for term, operation in zip(ast.terms, "++--+"):
            self.assertEqual(term.operation, operation)
        self.assertEqual(ast.terms[0].expr.value, 1)
        self.assertEqual(ast.terms[1].expr.name, "a")
        self.assertEqual(ast.terms[2].expr.value, 4)
        self.assertEqual(ast.terms[3].expr.value, 3)
        self.assertEqual(ast.terms[4].expr.name, "test")

    def testMulAndDiv(self):
        ast = self.parseExpression("1 * a / 4 / 3 * test")
        self.assertIsInstance(ast, parser.MulDivExprAST)
        for term, operation in zip(ast.terms, "**//*"):
            self.assertEqual(term.operation, operation)
        self.assertEqual(ast.terms[0].expr.value, 1)
        self.assertEqual(ast.terms[1].expr.name, "a")
        self.assertEqual(ast.terms[2].expr.value, 4)
        self.assertEqual(ast.terms[3].expr.value, 3)
        self.assertEqual(ast.terms[4].expr.name, "test")

    def testContant(self):
        ast = self.parseExpression("123")
        self.assertIsInstance(ast, parser.ConstIntAST)
        self.assertEqual(ast.value, 123)

    def testVariable(self):
        ast = self.parseExpression("qwe")
        self.assertIsInstance(ast, parser.VariableAST)

    def testConstantInBrackets(self):
        ast = self.parseExpression("((9))")
        self.assertIsInstance(ast, parser.ConstIntAST)
        self.assertEqual(ast.value, 9)

    def testFunctionCallInExpression(self):
        ast = self.parseExpression("(3+5)*@test(12+a)")
        self.assertIsInstance(ast, parser.MulDivExprAST)
        self.assertIsInstance(ast.terms[1].expr, parser.FunctionCallAST)
        self.assertEqual(ast.terms[1].expr.functionName, "test")
        self.assertEqual(len(ast.terms[1].expr.arguments), 1)
        self.assertEqual(ast.terms[1].expr.arguments[0].terms[0].expr.value, 12)

    def parseExpression(self, code):
        tokens = tokenize(code)
        ast = parser.parseExpression(tokens)
        self.assertIsInstance(ast, parser.ExpressionAST)
        return ast