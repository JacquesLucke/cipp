from . lexing import cippLexer
from . token_stream import TokenStream
from . tokens import IdentifierToken, IntegerToken, SingleCharToken

def astFromString(string):
    tokens = TokenStream(cippLexer.tokenize(string))
    return parseProgram(tokens)

def parseProgram(tokens):
    functions = []
    while nextIsKeyword(tokens, "def"):
        function = parseFunction(tokens)
        functions.append(function)
    return CippProgramAST(functions)

def parseFunction(tokens):
    acceptKeyword(tokens, "def")
    retType = parseType(tokens)
    acceptLetter(tokens, "@")
    name = acceptIdentifier(tokens)
    arguments = parseArguments(tokens)
    statement = parseStatement(tokens)
    return CippFunctionAST(name, retType, arguments, statement)

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
    return CippArgumentAST(name, dataType)

def parseType(tokens):
    dataType = acceptIdentifier(tokens)
    return CippTypeAST(dataType)

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
        return CippBlockStmtAST(statements)

def parseStatement_Return(tokens):
    acceptKeyword(tokens, "return")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return CippReturnStmtAST(expression)

def parseStatement_Let(tokens):
    acceptKeyword(tokens, "let")
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    acceptLetter(tokens, "=")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return CippLetStmtAST(name, dataType, expression)

def parseStatement_Assignment(tokens):
    targetName = acceptIdentifier(tokens)
    if nextIsLetter(tokens, "["):
        acceptLetter(tokens, "[")
        offset = parseExpression(tokens)
        acceptLetter(tokens, "]")
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return CippArrayAssignmentStmtAST(targetName, offset, expression)
    else:
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return CippAssignmentStmtAST(targetName, expression)

def parseStatement_While(tokens):
    acceptKeyword(tokens, "while")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    statement = parseStatement(tokens)
    return CippWhileStmtAST(condition, statement)

def parseStatement_If(tokens):
    acceptKeyword(tokens, "if")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    thenStatement = parseStatement(tokens)
    if nextIsKeyword(tokens, "else"):
        acceptKeyword(tokens, "else")
        elseStatement = parseStatement(tokens)
        return CippIfElseStmtAST(condition, thenStatement, elseStatement)
    else:
        return CippIfStmtAST(condition, thenStatement)

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
        return CippComparisonAST(operator, expressionLeft, expressionRight)
    else:
        return expressionLeft

def nextIsComparisonOperator(tokens):
    return nextIsOneOfLetters(tokens, "<", ">", "=", "!")

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
    addTerms = []
    subTerms = []

    term = parseExpression_MulDivLevel(tokens)
    addTerms.append(term)

    while nextIsOneOfLetters(tokens, "+", "-"):
        if nextIsLetter(tokens, "+"):
            acceptLetter(tokens, "+")
            term = parseExpression_MulDivLevel(tokens)
            addTerms.append(term)
        elif nextIsLetter(tokens, "-"):
            acceptLetter(tokens, "-")
            term = parseExpression_MulDivLevel(tokens)
            subTerms.append(term)

    if len(addTerms) == 1 and len(subTerms) == 0:
        return addTerms[0]
    else:
        return CippAddSubExprAST(addTerms, subTerms)

def parseExpression_MulDivLevel(tokens):
    mulFactors = []
    divFactors = []

    factor = parseExpression_FactorLevel(tokens)
    mulFactors.append(factor)

    while nextIsOneOfLetters(tokens, "*", "/"):
        if nextIsLetter(tokens, "*"):
            acceptLetter(tokens, "*")
            factor = parseExpression_FactorLevel(tokens)
            mulFactors.append(factor)
        elif nextIsLetter(tokens, "/"):
            acceptLetter(tokens, "/")
            factor = parseExpression_FactorLevel(tokens)
            divFactors.append(factor)
    
    if len(mulFactors) == 1 and len(divFactors) == 0:
        return mulFactors[0]
    else:
        return CippMulDivExprAST(mulFactors, divFactors)

def parseExpression_FactorLevel(tokens):
    if nextIsIdentifier(tokens):
        name = acceptIdentifier(tokens)
        return CippVariableAST(name)
    elif nextIsInteger(tokens):
        value = acceptInteger(tokens)
        return CippConstIntAST(value)
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
    return CippFunctionCallAST(name, arguments)

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


class CippProgramAST:
    def __init__(self, functions):
        self.functions = functions

class CippFunctionAST:
    def __init__(self, name, retType, arguments, statement):
        self.name = name
        self.retType = retType
        self.arguments = arguments
        self.statement = statement

    def __repr__(self):
        return f"<{self.retType} {self.name}({self.arguments})>"

class CippTypeAST:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class CippArgumentAST:
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType

    def __repr__(self):
        return f"{self.dataType} {self.name}"

class CippStmtAST:
    pass

class CippBlockStmtAST(CippStmtAST):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "\n".join(map(str, self.statements))

class CippReturnStmtAST(CippStmtAST):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"return {self.expression}"

class CippLetStmtAST(CippStmtAST):
    def __init__(self, name, dataType, expression):
        self.name = name
        self.dataType = dataType
        self.expression = expression

    def __repr__(self):
        return f"let {self.dataType} {self.name} = {self.expression}"

class CippWhileStmtAST(CippStmtAST):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def __repr__(self):
        return f"while ({self.condition}) ..."

class CippIfStmtAST(CippStmtAST):
    def __init__(self, condition, thenStatement):
        self.condition = condition
        self.thenStatement = thenStatement

    def __repr__(self):
        return f"if ({self.condition}) ..."

class CippIfElseStmtAST(CippStmtAST):
    def __init__(self, condition, thenStatement, elseStatement):
        self.condition = condition
        self.thenStatement = thenStatement
        self.elseStatement = elseStatement

    def __repr__(self):
        return f"if ({self.condition}) ...\nelse ..."

class CippAssignmentStmtAST:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __repr__(self):
        return f"{self.target} = {self.expression}"

class CippArrayAssignmentStmtAST:
    def __init__(self, target, offset, expression):
        self.target = target
        self.offset = offset
        self.expression = expression

    def __repr__(self):
        return f"{self.target}[{self.offset}] = {self.expression}"

class CippExpressionAST:
    pass

class CippComparisonAST(CippExpressionAST):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left 
        self.right = right

    def __repr__(self):
        return f"{self.left}{self.operator}{self.right}"

class CippAddSubExprAST(CippExpressionAST):
    def __init__(self, addTerms, subTerms):
        self.addTerms = addTerms
        self.subTerms = subTerms

    def __repr__(self):
        addPart = "+".join(self.addTerms)
        subPart = "-".join(self.subTerms)
        if len(addPart) == 0:
            return f"-{subPart}"
        elif len(subPart) == 0:
            return addPart
        else:
            return f"{addPart}-{subPart}"

class CippMulDivExprAST(CippExpressionAST):
    def __init__(self, mulFactors, divFactors):
        self.mulFactors = mulFactors
        self.divFactors = divFactors

    def __repr__(self):
        mulPart = "*".join(self.mulFactors)
        divPart = "/".join(self.divFactors)
        if len(mulPart) == 0:
            return f"1/{divPart}"
        elif len(divPart) == 0:
            return mulPart
        else:
            return f"{mulPart} / {divPart}"

class CippVariableAST(CippExpressionAST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class CippConstIntAST(CippExpressionAST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class CippFunctionCallAST(CippExpressionAST):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"@{self.name}({', '.join(self.arguments)})"