from . lexing import clippLexer
from . token_stream import TokenStream
from . tokens import IdentifierToken, IntegerToken, SingleCharToken

def astFromString(string):
    tokens = TokenStream(list(clippLexer.tokenize(string)))
    return parseProgram(tokens)

def parseProgram(tokens):
    functions = []
    while nextIsKeyword(tokens, "def"):
        function = parseFunction(tokens)
        functions.append(function)
    return ClippProgramAST(functions)

def parseFunction(tokens):
    acceptKeyword(tokens, "def")
    retType = parseType(tokens)
    acceptLetter(tokens, "@")
    name = acceptIdentifier(tokens)
    arguments = parseArguments(tokens)
    statement = parseStatement(tokens)
    return ClippFunctionAST(name, retType, arguments, statement)

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
    return ClippArgumentAST(name, dataType)

def parseType(tokens):
    dataType = acceptIdentifier(tokens)
    return ClippTypeAST(dataType)

def parseStatement(tokens):
    if nextIsLetter(tokens, "{"):
        return parseBlockStatement(tokens)
    elif nextIsKeyword(tokens, "return"):
        return parseReturnStatement(tokens)
    elif nextIsKeyword(tokens, "let"):
        return parseLetStatement(tokens)
    elif nextIsKeyword(tokens, "while"):
        return parseWhileStatement(tokens)
    elif nextIsKeyword(tokens, "if"):
        return parseIfStatement(tokens)
    elif nextIsIdentifier(tokens):
        return parseAssignentStatement(tokens)
    else:
        raise Exception("unknown statement type")

def parseBlockStatement(tokens, a = 0):
    statements = []
    acceptLetter(tokens, "{")
    while not nextIsLetter(tokens, "}"):
        statement = parseStatement(tokens)
        statements.append(statement)
    acceptLetter(tokens, "}")
    return ClippBlockStmtAST(statements)

def parseReturnStatement(tokens):
    acceptKeyword(tokens, "return")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return ClippReturnStmtAST(expression)

def parseLetStatement(tokens):
    acceptKeyword(tokens, "let")
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    acceptLetter(tokens, "=")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return ClippLetStmtAST(name, dataType, expression)

def parseAssignentStatement(tokens):
    targetName = acceptIdentifier(tokens)
    if nextIsLetter(tokens, "["):
        acceptLetter(tokens, "[")
        offset = parseExpression(tokens)
        acceptLetter(tokens, "]")
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return ClippArrayAssignmentStmtAST(targetName, offset, expression)
    else:
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return ClippAssignmentStmtAST(targetName, expression)

def parseWhileStatement(tokens):
    acceptKeyword(tokens, "while")
    acceptLetter(tokens, "(")
    condition = parseCondition(tokens)
    acceptLetter(tokens, ")")
    statement = parseStatement(tokens)
    return ClippWhileStmtAST(condition, statement)

def parseIfStatement(tokens):
    acceptKeyword(tokens, "if")
    acceptLetter(tokens, "(")
    condition = parseCondition(tokens)
    acceptLetter(tokens, ")")
    thenStatement = parseStatement(tokens)
    if nextIsKeyword(tokens, "else"):
        acceptKeyword(tokens, "else")
        elseStatement = parseStatement(tokens)
        return ClippIfElseStmtAST(condition, thenStatement, elseStatement)
    else:
        return ClippIfStmtAST(condition, thenStatement)

def parseCondition(tokens):
    return parseComparison(tokens)

def parseComparison(tokens):
    left = parseExpression(tokens)
    operator = parseComparisonOperator(tokens)
    right = parseExpression(tokens)
    return ClippComparisonAST(operator, left, right)

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

def parseExpression(tokens):
    addTerms = []
    subTerms = []

    term = parseTerm(tokens)
    addTerms.append(term)

    while nextIsOneOfLetters(tokens, "+", "-"):
        if nextIsLetter(tokens, "+"):
            acceptLetter(tokens, "+")
            term = parseTerm(tokens)
            addTerms.append(term)
        elif nextIsLetter(tokens, "-"):
            acceptLetter(tokens, "-")
            term = parseTerm(tokens)
            subTerms.append(term)

    return ClippAddSubExprAST(addTerms, subTerms)

def parseTerm(tokens):
    mulFactors = []
    divFactors = []

    factor = parseFactor(tokens)
    mulFactors.append(factor)

    while nextIsOneOfLetters(tokens, "*", "/"):
        if nextIsLetter(tokens, "*"):
            acceptLetter(tokens, "*")
            factor = parseFactor(tokens)
            mulFactors.append(factor)
        elif nextIsLetter(tokens, "/"):
            acceptLetter(tokens, "/")
            factor = parseFactor(tokens)
            divFactors.append(factor)
    
    return ClippMulDivExprAST(mulFactors, divFactors)

def parseFactor(tokens):
    if nextIsIdentifier(tokens):
        name = acceptIdentifier(tokens)
        return ClippVariableAST(name)
    elif nextIsInteger(tokens):
        value = acceptInteger(tokens)
        return ClippConstIntAST(value)
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
    return ClippFunctionCallAST(name, arguments)

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


class ClippProgramAST:
    def __init__(self, functions):
        self.functions = functions

class ClippFunctionAST:
    def __init__(self, name, retType, arguments, statement):
        self.name = name
        self.retType = retType
        self.arguments = arguments
        self.statement = statement

    def __repr__(self):
        return f"<{self.retType} {self.name}({self.arguments})>"

class ClippTypeAST:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class ClippArgumentAST:
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType

    def __repr__(self):
        return f"{self.dataType} {self.name}"

class ClippStmtAST:
    pass

class ClippBlockStmtAST(ClippStmtAST):
    def __init__(self, statements):
        self.statements = statements

class ClippReturnStmtAST(ClippStmtAST):
    def __init__(self, expression):
        self.expression = expression

class ClippLetStmtAST(ClippStmtAST):
    def __init__(self, name, dataType, expression):
        self.name = name
        self.dataType = dataType
        self.expression = expression

class ClippWhileStmtAST(ClippStmtAST):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

class ClippIfStmtAST(ClippStmtAST):
    def __init__(self, condition, thenStatement):
        self.condition = condition
        self.thenStatement = thenStatement

class ClippIfElseStmtAST(ClippStmtAST):
    def __init__(self, condition, thenStatement, elseStatement):
        self.condition = condition
        self.thenStatement = thenStatement
        self.elseStatement = elseStatement

class ClippAssignmentStmtAST:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

class ClippArrayAssignmentStmtAST:
    def __init__(self, target, offset, expression):
        self.target = target
        self.offset = offset
        self.expression = expression

class ClippComparisonAST:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left 
        self.right = right

class ClippAddSubExprAST:
    def __init__(self, addTerms, subTerms):
        self.addTerms = addTerms
        self.subTerms = subTerms

class ClippMulDivExprAST:
    def __init__(self, mulFactors, divFactors):
        self.mulFactors = mulFactors
        self.divFactors = divFactors

class ClippVariableAST:
    def __init__(self, name):
        self.name = name

class ClippConstIntAST:
    def __init__(self, value):
        self.value = value

class ClippFunctionCallAST:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments