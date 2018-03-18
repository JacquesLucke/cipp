import unittest
from . import ast
from . import parser
tokenize = parser.stringToTokenStream

class TestSelectStatementParser(unittest.TestCase):
    def testBlock(self):
        stmt = self.parseStatement("{a=b;c=d;}")
        self.assertIsInstance(stmt, ast.BlockStmt)

    def testReturn(self):
        stmt = self.parseStatement("return 3;")
        self.assertIsInstance(stmt, ast.ReturnStmt)

    def testLet(self):
        stmt = self.parseStatement("let int variable = 42;")
        self.assertIsInstance(stmt, ast.LetStmt)

    def testWhile(self):
        stmt = self.parseStatement("while (1 < 2) {}")
        self.assertIsInstance(stmt, ast.WhileStmt)

    def testIf(self):
        stmt = self.parseStatement("if (1 < 2) {}")
        self.assertIsInstance(stmt, ast.IfStmt)

    def testIfElse(self):
        stmt = self.parseStatement("if (1) {} else {}")
        self.assertIsInstance(stmt, ast.IfElseStmt)

    def parseStatement(self, code):
        tokens = tokenize(code)
        return parser.parseStatement(tokens)

class TestParseFunctionCall(unittest.TestCase):
    def testNormal(self):
        node = self.parseFunctionCall("@hello(3+4, 2*a)")
        self.assertEqual(node.functionName, "hello")
        self.assertEqual(len(node.arguments), 2)

    def testMissingAt(self):
        with self.assertRaises(Exception):
            self.parseFunctionCall("hello(1, 1)")

    def testNoArguments(self):
        node = self.parseFunctionCall("@test()")
        self.assertEqual(node.functionName, "test")
        self.assertEqual(len(node.arguments), 0)  

    def testForgottenComma(self):
        with self.assertRaises(Exception):
            self.parseFunctionCall("@test(2 3)")    

    def parseFunctionCall(self, code):
        tokens = tokenize(code)
        node = parser.parseFunctionCall(tokens)
        self.assertIsInstance(node, ast.FunctionCall)
        return node

class TestParseExpression(unittest.TestCase):
    def testSimpleAdd(self):
        node = self.parseExpression("3 + a")
        self.assertIsInstance(node, ast.AddSubExpr)
        self.assertEqual(node.terms[0].expr.value, 3)
        self.assertEqual(node.terms[1].expr.name, "a")

    def testAddAndSub(self):
        node = self.parseExpression("1 + a - 4 - 3 + test")
        self.assertIsInstance(node, ast.AddSubExpr)
        for term, operation in zip(node.terms, "++--+"):
            self.assertEqual(term.operation, operation)
        self.assertEqual(node.terms[0].expr.value, 1)
        self.assertEqual(node.terms[1].expr.name, "a")
        self.assertEqual(node.terms[2].expr.value, 4)
        self.assertEqual(node.terms[3].expr.value, 3)
        self.assertEqual(node.terms[4].expr.name, "test")

    def testMulAndDiv(self):
        node = self.parseExpression("1 * a / 4 / 3 * test")
        self.assertIsInstance(node, ast.MulDivExpr)
        for term, operation in zip(node.terms, "**//*"):
            self.assertEqual(term.operation, operation)
        self.assertEqual(node.terms[0].expr.value, 1)
        self.assertEqual(node.terms[1].expr.name, "a")
        self.assertEqual(node.terms[2].expr.value, 4)
        self.assertEqual(node.terms[3].expr.value, 3)
        self.assertEqual(node.terms[4].expr.name, "test")

    def testContant(self):
        node = self.parseExpression("123")
        self.assertIsInstance(node, ast.ConstInt)
        self.assertEqual(node.value, 123)

    def testVariable(self):
        node = self.parseExpression("qwe")
        self.assertIsInstance(node, ast.Variable)

    def testConstantInBrackets(self):
        node = self.parseExpression("((9))")
        self.assertIsInstance(node, ast.ConstInt)
        self.assertEqual(node.value, 9)

    def testFunctionCallInExpression(self):
        node = self.parseExpression("(3+5)*@test(12+a)")
        self.assertIsInstance(node, ast.MulDivExpr)
        self.assertIsInstance(node.terms[1].expr, ast.FunctionCall)
        self.assertEqual(node.terms[1].expr.functionName, "test")
        self.assertEqual(len(node.terms[1].expr.arguments), 1)
        self.assertEqual(node.terms[1].expr.arguments[0].terms[0].expr.value, 12)

    def parseExpression(self, code):
        tokens = tokenize(code)
        node = parser.parseExpression(tokens)
        self.assertIsInstance(node, ast.Expression)
        return node