from . import ast
from . lexer import Lexer
from . token_stream import TokenStream

from . tokens import (
    createSingleCharToken,
    IdentifierToken, IntegerToken,
    CommentToken, WhitespaceToken
)

SingleCharToken = createSingleCharToken("(){}[],=+-*/@;<>!")
cippLexer = Lexer(
    [IdentifierToken, IntegerToken, CommentToken, 
     SingleCharToken, WhitespaceToken], 
    ignoredTokens = [WhitespaceToken, CommentToken]
)

def parse(string):
    tokens = stringToTokenStream(string)
    return parseProgram(tokens)

def stringToTokenStream(string):
    return TokenStream(cippLexer.tokenize(string))

def parseProgram(tokens):
    functions = []
    while nextIsKeyword(tokens, "def"):
        function = parseFunction(tokens)
        functions.append(function)
    return ast.Program(functions)

def parseFunction(tokens):
    acceptKeyword(tokens, "def")
    retType = parseType(tokens)
    acceptLetter(tokens, "@")
    name = acceptIdentifier(tokens)
    arguments = parseArguments(tokens)
    statement = parseStatement(tokens)
    return ast.Function(name, retType, arguments, statement)

def parseArguments(tokens):
    return parseList(tokens, parseArgument, "(", ")", ",")

def parseArgument(tokens):
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    return ast.Argument(name, dataType)

def parseType(tokens):
    dataType = acceptIdentifier(tokens)
    return ast.Type(dataType)

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
    statements = parseList(tokens, parseStatement, "{", "}")
    if len(statements) == 1:
        return statements[0]
    else: 
        return ast.BlockStmt(statements)

def parseStatement_Return(tokens):
    acceptKeyword(tokens, "return")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return ast.ReturnStmt(expression)

def parseStatement_Let(tokens):
    acceptKeyword(tokens, "let")
    dataType = parseType(tokens)
    name = acceptIdentifier(tokens)
    acceptLetter(tokens, "=")
    expression = parseExpression(tokens)
    acceptLetter(tokens, ";")
    return ast.LetStmt(name, dataType, expression)

def parseStatement_Assignment(tokens):
    targetName = acceptIdentifier(tokens)
    if nextIsLetter(tokens, "["):
        acceptLetter(tokens, "[")
        offset = parseExpression(tokens)
        acceptLetter(tokens, "]")
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return ast.ArrayAssignmentStmt(targetName, offset, expression)
    else:
        acceptLetter(tokens, "=")
        expression = parseExpression(tokens)
        acceptLetter(tokens, ";")
        return ast.AssignmentStmt(targetName, expression)

def parseStatement_While(tokens):
    acceptKeyword(tokens, "while")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    statement = parseStatement(tokens)
    return ast.WhileStmt(condition, statement)

def parseStatement_If(tokens):
    acceptKeyword(tokens, "if")
    acceptLetter(tokens, "(")
    condition = parseExpression(tokens)
    acceptLetter(tokens, ")")
    thenStatement = parseStatement(tokens)
    if nextIsKeyword(tokens, "else"):
        acceptKeyword(tokens, "else")
        elseStatement = parseStatement(tokens)
        return ast.IfElseStmt(condition, thenStatement, elseStatement)
    else:
        return ast.IfStmt(condition, thenStatement)

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
        return ast.ComparisonExpr(operator, expressionLeft, expressionRight)
    else:
        return expressionLeft

comparisonOperators = ("==", "<=", ">=", "!=", "<", ">")
def parseComparisonOperator(tokens):
    for operator in comparisonOperators:
        if nextLettersAre(tokens, operator):
            acceptLetters(tokens, operator)
            return operator
    raise Exception("unknown comparison operator")

def parseExpression_AddSubLevel(tokens):
    terms = []

    term = parseExpression_MulDivLevel(tokens)
    terms.append(ast.AddedTerm(term))

    while nextIsOneOfLetters(tokens, "+", "-"):
        if nextIsLetter(tokens, "+"):
            acceptLetter(tokens, "+")
            term = parseExpression_MulDivLevel(tokens)
            terms.append(ast.AddedTerm(term))
        elif nextIsLetter(tokens, "-"):
            acceptLetter(tokens, "-")
            term = parseExpression_MulDivLevel(tokens)
            terms.append(ast.SubtractedTerm(term))

    if len(terms) == 1 and isinstance(terms[0], ast.AddedTerm):
        return terms[0].expr
    else:
        return ast.AddSubExpr(terms)

def parseExpression_MulDivLevel(tokens):
    terms = []

    factor = parseExpression_FactorLevel(tokens)
    terms.append(ast.MultipliedTerm(factor))

    while nextIsOneOfLetters(tokens, "*", "/"):
        if nextIsLetter(tokens, "*"):
            acceptLetter(tokens, "*")
            factor = parseExpression_FactorLevel(tokens)
            terms.append(ast.MultipliedTerm(factor))
        elif nextIsLetter(tokens, "/"):
            acceptLetter(tokens, "/")
            factor = parseExpression_FactorLevel(tokens)
            terms.append(ast.DividedTerm(factor))
    
    if len(terms) == 1 and isinstance(terms[0], ast.MultipliedTerm):
        return terms[0].expr
    else:
        return ast.MulDivExpr(terms)

def parseExpression_FactorLevel(tokens):
    if nextIsIdentifier(tokens):
        name = acceptIdentifier(tokens)
        return ast.Variable(name)
    elif nextIsInteger(tokens):
        value = acceptInteger(tokens)
        return ast.ConstInt(value)
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
    return ast.FunctionCall(name, arguments)

def parseCallArguments(tokens):
    return parseList(tokens, parseExpression, "(", ")", ",")

def parseList(tokens, parseElement, start, end, separator = None):
    elements = []
    acceptLetter(tokens, start)
    while not nextIsLetter(tokens, end):
        element = parseElement(tokens)
        elements.append(element)
        if separator is None:
            if nextIsLetter(tokens, end):
                break
        else:
            if nextIsLetter(tokens, separator):
                acceptLetter(tokens, separator)
            else:
                break
    acceptLetter(tokens, end)
    return elements



# Utility Functions
####################################################

def acceptKeyword(tokens, keyword):
    if nextIsKeyword(tokens, keyword):
        tokens.takeNext()
    else:
        raise Exception(f"expected keyword '{keyword}'")

def acceptLetters(tokens, letters):
    for letter in letters:
        acceptLetter(tokens, letter)

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

def nextLettersAre(tokens, letters):
    if len(tokens) < len(letters): return False
    for token, letter in zip(tokens.getLookahead(len(letters)), letters):
        if not isinstance(token, SingleCharToken) or token.value != letter:
            return False
    return True

def nextIsIdentifier(tokens):
    if len(tokens) == 0: return False
    return isinstance(tokens.peekNext(), IdentifierToken)

def nextIsInteger(tokens):
    if len(tokens) == 0: return False
    return isinstance(tokens.peekNext(), IntegerToken)

def nextIsComparisonOperator(tokens):
    return any(nextLettersAre(tokens, s) for s in comparisonOperators)