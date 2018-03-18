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

class ComparisonExprAST(ExpressionAST):
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