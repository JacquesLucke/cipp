class Program:
    def __init__(self, functions):
        self.functions = functions

class Function:
    def __init__(self, name, retType, arguments, statement):
        self.name = name
        self.retType = retType
        self.arguments = arguments
        self.statement = statement

    def __repr__(self):
        return f"<{self.retType} {self.name}({self.arguments})>"

class Type:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Argument:
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType

    def __repr__(self):
        return f"{self.dataType} {self.name}"



class Statement:
    pass

class BlockStmt(Statement):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "\n".join(map(str, self.statements))

class ReturnStmt(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"return {self.expression}"

class LetStmt(Statement):
    def __init__(self, name, dataType, expression):
        self.name = name
        self.dataType = dataType
        self.expression = expression

    def __repr__(self):
        return f"let {self.dataType} {self.name} = {self.expression}"

class WhileStmt(Statement):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def __repr__(self):
        return f"while ({self.condition}) ..."

class IfStmt(Statement):
    def __init__(self, condition, thenStatement):
        self.condition = condition
        self.thenStatement = thenStatement

    def __repr__(self):
        return f"if ({self.condition}) ..."

class IfElseStmt(Statement):
    def __init__(self, condition, thenStatement, elseStatement):
        self.condition = condition
        self.thenStatement = thenStatement
        self.elseStatement = elseStatement

    def __repr__(self):
        return f"if ({self.condition}) ...\nelse ..."

class AssignmentStmt(Statement):
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __repr__(self):
        return f"{self.target} = {self.expression}"

class ArrayAssignmentStmt(Statement):
    def __init__(self, target, offset, expression):
        self.target = target
        self.offset = offset
        self.expression = expression

    def __repr__(self):
        return f"{self.target}[{self.offset}] = {self.expression}"



class Expression:
    pass

class ComparisonExpr(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left 
        self.right = right

    def __repr__(self):
        return f"{self.left}{self.operator}{self.right}"

class AddSubExpr(Expression):
    def __init__(self, termsWithType):
        self.terms = termsWithType

    def __repr__(self):
        string = ""
        for term in self.terms:
            string += term.operation + str(term.expr)
        return string

class MulDivExpr(Expression):
    def __init__(self, termsWithType):
        self.terms = termsWithType

    def __repr__(self):
        string = ""
        for term in self.terms:
            string += term.operation + str(term.expr)
        return string

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class ConstInt(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class FunctionCall(Expression):
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