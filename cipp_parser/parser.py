from . lexing import cippLexer
from . token_stream import TokenStream
from . tokens import IdentifierToken, IntegerToken, SingleCharToken

def astFromString(string):
    tokens = stringToTokenStream(string)
    return parseProgram(tokens)

def stringToTokenStream(string):
    return TokenStream(cippLexer.tokenize(string))

def parseProgram(tokens):
    functions = []
    while nextIsKeyword(tokens, "def"):
        function = parseFunction(tokens)
        functions.append(function)
    return ProgramAST(functions)

def parseFunction(tokens):
    acceptKeyword(tokens, "def")
    retType = parseType(tokens)
    acceptLetter(tokens, "@")
    name = acceptIdentifier(tokens)
    arguments = parseArguments(tokens)
    statement = parseStatement(tokens)
    return FunctionAST(name, retType, arguments, statement)

def parseArguments(tokens):
    acceptLetter(tokens, "(")
    if nextIsLetter(tokens, ")"):
        acceptLetter(tokens, ")")
        return []
    else:
        arguments = []
        while True:
            argument = parseArgument(tokens)
            arguments.append(argument)
            if nextIsLetter(tokens, ","):
                acceptLetter(tokens, ",")
                continue
            else:
                break
        acceptLetter(tokens, ")")
        return arguments

def parseArgument(tokens):
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    return ArgumentAST(name, dataType)

def parseType(tokens):
    dataType = acceptIdentifier(tokens)
    return TypeAST(dataType)

def parseStatement(tokens):
    if nextIsLetter(tokens, "{"):
        return parseStatement_Block(tokens)
    elif nextIsKeyword(tokens, "return"):
        return parseStatement_Return(tokens)
    elif nextIsKeyword(tokens, "let"):
        return parseStatement_Let(tokens)
    elif nextIsKeyword(tokens, "while"):
        return parseStatement_While(tokens)
    elif nextIsKeyword(tokens, "if"):
        return parseStatement_If(tokens)
    elif nextIsIdentifier(tokens):
        return parseStatement_Assignment(tokens)
    else:
        raise Exception("unknown statement type")

def parseStatement_Block(tokens, a = 0):
    statements = []
    acceptLetter(tokens, "{")
    while not nextIsLetter(tokens, "}"):
        statement = parseStatement(tokens)
        statements.append(statement)
    acceptLetter(tokens, "}")

    if len(statements) == 1:
        return statements[0]
    else:
        return BlockStmtAST(statements)

def parseStatement_Return(tokens):
    acceptKeyword(tokens, "return")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return ReturnStmtAST(expression)

def parseStatement_Let(tokens):
    acceptKeyword(tokens, "let")
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    acceptLetter(tokens, "=")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return LetStmtAST(name, dataType, expression)

def parseStatement_Assignment(tokens):
    targetName = acceptIdentifier(tokens)
    if nextIsLetter(tokens, "["):
        acceptLetter(tokens, "[")
        offset = parseExpression(tokens)
        acceptLetter(tokens, "]")
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return ArrayAssignmentStmtAST(targetName, offset, expression)
    else:
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return AssignmentStmtAST(targetName, expression)

def parseStatement_While(tokens):
    acceptKeyword(tokens, "while")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    statement = parseStatement(tokens)
    return WhileStmtAST(condition, statement)

def parseStatement_If(tokens):
    acceptKeyword(tokens, "if")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    thenStatement = parseStatement(tokens)
    if nextIsKeyword(tokens, "else"):
        acceptKeyword(tokens, "else")
        elseStatement = parseStatement(tokens)
        return IfElseStmtAST(condition, thenStatement, elseStatement)
    else:
        return IfStmtAST(condition, thenStatement)

def parseExpression(tokens):
    '''
    Expression parsing happens at different levels
    because of operator precedence rules.
    '''
    return parseExpression_ComparisonLevel(tokens)

def parseExpression_ComparisonLevel(tokens):
    expressionLeft = parseExpression_AddSubLevel(tokens)
    if nextIsComparisonOperator(tokens):
        operator = parseComparisonOperator(tokens)
        expressionRight = parseExpression_AddSubLevel(tokens)
        return ComparisonAST(operator, expressionLeft, expressionRight)
    else:
        return expressionLeft

def parseComparisonOperator(tokens):
    if nextIsLetter(tokens, "="):
        acceptLetter(tokens, "=")
        acceptLetter(tokens, "=")
        return "=="
    elif nextIsLetter(tokens, "<"):
        acceptLetter(tokens, "<")
        if nextIsLetter(tokens, "="):
            acceptLetter(tokens, "=")
            return "<="
        else:
            return "<"
    elif nextIsLetter(tokens, ">"):
        acceptLetter(tokens, ">")
        if nextIsLetter(tokens, "="):
            acceptLetter(tokens, "=")
            return ">="
        else:
            return ">"
    elif nextIsLetter(tokens, "!"):
        acceptLetter(tokens, "!")
        acceptLetter(tokens, "=")
        return "!="

def parseExpression_AddSubLevel(tokens):
    terms = []

    term = parseExpression_MulDivLevel(tokens)
    terms.append(AddedTerm(term))

    while nextIsOneOfLetters(tokens, "+", "-"):
        if nextIsLetter(tokens, "+"):
            acceptLetter(tokens, "+")
            term = parseExpression_MulDivLevel(tokens)
            terms.append(AddedTerm(term))
        elif nextIsLetter(tokens, "-"):
            acceptLetter(tokens, "-")
            term = parseExpression_MulDivLevel(tokens)
            terms.append(SubtractedTerm(term))

    if len(terms) == 1 and isinstance(terms[0], AddedTerm):
        return terms[0].expr
    else:
        return AddSubExprAST(terms)

def parseExpression_MulDivLevel(tokens):
    terms = []

    factor = parseExpression_FactorLevel(tokens)
    terms.append(MultipliedTerm(factor))

    while nextIsOneOfLetters(tokens, "*", "/"):
        if nextIsLetter(tokens, "*"):
            acceptLetter(tokens, "*")
            factor = parseExpression_FactorLevel(tokens)
            terms.append(MultipliedTerm(factor))
        elif nextIsLetter(tokens, "/"):
            acceptLetter(tokens, "/")
            factor = parseExpression_FactorLevel(tokens)
            terms.append(DividedTerm(factor))
    
    if len(terms) == 1 and isinstance(terms[0], MultipliedTerm):
        return terms[0].expr
    else:
        return MulDivExprAST(terms)

def parseExpression_FactorLevel(tokens):
    if nextIsIdentifier(tokens):
        name = acceptIdentifier(tokens)
        return VariableAST(name)
    elif nextIsInteger(tokens):
        value = acceptInteger(tokens)
        return ConstIntAST(value)
    elif nextIsLetter(tokens, "("):
        acceptLetter(tokens, "(")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ")")
        return expression
    elif nextIsLetter(tokens, "@"):
        return parseFunctionCall(tokens)

def parseFunctionCall(tokens):
    acceptLetter(tokens, "@")
    name = acceptIdentifier(tokens)
    arguments = parseCallArguments(tokens)
    return FunctionCallAST(name, arguments)

def parseCallArguments(tokens):
    acceptLetter(tokens, "(")
    if nextIsLetter(tokens, ")"):
        return []
    else:
        arguments = []
        while True:
            expression = parseExpression(tokens)
            arguments.append(expression)
            if nextIsLetter(tokens, ","):
                acceptLetter(tokens, ",")
                continue
            else:
                break
        acceptLetter(tokens, ")")
        return arguments


def nextIsKeyword(tokens, keyword):
    if len(tokens) == 0: return False
    nextToken = tokens.peekNext()
    if isinstance(nextToken, IdentifierToken):
        return nextToken.value == keyword
    return False

def nextIsLetter(tokens, letter):
    if len(tokens) == 0: return False
    nextToken = tokens.peekNext()
    if isinstance(nextToken, SingleCharToken):
        return nextToken.value == letter
    return False

def nextIsOneOfLetters(tokens, *letters):
    return any(nextIsLetter(tokens, c) for c in letters)

def nextIsIdentifier(tokens):
    if len(tokens) == 0: return False
    return isinstance(tokens.peekNext(), IdentifierToken)

def nextIsInteger(tokens):
    if len(tokens) == 0: return False
    return isinstance(tokens.peekNext(), IntegerToken)

def nextIsComparisonOperator(tokens):
    return nextIsOneOfLetters(tokens, "<", ">", "=", "!")


def acceptKeyword(tokens, keyword):
    if nextIsKeyword(tokens, keyword):
        tokens.takeNext()
    else:
        raise Exception(f"expected keyword '{keyword}'")

def acceptLetter(tokens, letter):
    if nextIsLetter(tokens, letter):
        tokens.takeNext()
    else:
        raise Exception(f"expected token '{letter}'")

def acceptIdentifier(tokens):
    if nextIsIdentifier(tokens):
        return tokens.takeNext().value
    else:
        raise Exception("expected identifier")

def acceptInteger(tokens):
    if nextIsInteger(tokens):
        return tokens.takeNext().value
    else:
        raise Exception("expected integer")


class ProgramAST:
    def __init__(self, functions):
        self.functions = functions

class FunctionAST:
    def __init__(self, name, retType, arguments, statement):
        self.name = name
        self.retType = retType
        self.arguments = arguments
        self.statement = statement

    def __repr__(self):
        return f"<{self.retType} {self.name}({self.arguments})>"

class TypeAST:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class ArgumentAST:
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType

    def __repr__(self):
        return f"{self.dataType} {self.name}"

class StmtAST:
    pass

class BlockStmtAST(StmtAST):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "\n".join(map(str, self.statements))

class ReturnStmtAST(StmtAST):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"return {self.expression}"

class LetStmtAST(StmtAST):
    def __init__(self, name, dataType, expression):
        self.name = name
        self.dataType = dataType
        self.expression = expression

    def __repr__(self):
        return f"let {self.dataType} {self.name} = {self.expression}"

class WhileStmtAST(StmtAST):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def __repr__(self):
        return f"while ({self.condition}) ..."

class IfStmtAST(StmtAST):
    def __init__(self, condition, thenStatement):
        self.condition = condition
        self.thenStatement = thenStatement

    def __repr__(self):
        return f"if ({self.condition}) ..."

class IfElseStmtAST(StmtAST):
    def __init__(self, condition, thenStatement, elseStatement):
        self.condition = condition
        self.thenStatement = thenStatement
        self.elseStatement = elseStatement

    def __repr__(self):
        return f"if ({self.condition}) ...\nelse ..."

class AssignmentStmtAST:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __repr__(self):
        return f"{self.target} = {self.expression}"

class ArrayAssignmentStmtAST:
    def __init__(self, target, offset, expression):
        self.target = target
        self.offset = offset
        self.expression = expression

    def __repr__(self):
        return f"{self.target}[{self.offset}] = {self.expression}"

class ExpressionAST:
    pass

class ComparisonAST(ExpressionAST):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left 
        self.right = right

    def __repr__(self):
        return f"{self.left}{self.operator}{self.right}"

class AddSubExprAST(ExpressionAST):
    def __init__(self, termsWithType):
        self.terms = termsWithType

    def __repr__(self):
        string = ""
        for term in self.terms:
            string += term.operation + str(term.expr)
        return string

class MulDivExprAST(ExpressionAST):
    def __init__(self, termsWithType):
        self.terms = termsWithType

    def __repr__(self):
        string = ""
        for term in self.terms:
            string += term.operation + str(term.expr)
        return string

class VariableAST(ExpressionAST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class ConstIntAST(ExpressionAST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class FunctionCallAST(ExpressionAST):
    def __init__(self, functionName, arguments):
        self.functionName = functionName
        self.arguments = arguments

    def __repr__(self):
        return f"@{self.functionName}({', '.join(self.arguments)})"


class AddedTerm:
    operation = "+"
    def __init__(self, expression):
        self.expr = expression
class SubtractedTerm:
    operation = "-"
    def __init__(self, expression):
        self.expr = expression
class MultipliedTerm:
    operation = "*"
    def __init__(self, expression):
        self.expr = expression
class DividedTerm:
    operation = "/"
    def __init__(self, expression):
        self.expr = expression