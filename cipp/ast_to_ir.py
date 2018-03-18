from . import ir
from . import ast

def transformProgramToIR(programAST):
    functionsIRs = list(map(transformFunctionToIR, programAST.functions))
    return ir.Module(functionsIRs)

def transformFunctionToIR(functionAST):
    functionIR = ir.Function(functionAST.name)

    variables = {}
    for argument in functionAST.arguments:
        variables[argument.name] = functionIR.addArgument()

    insertInstr_Statement(functionIR.block, functionAST.statement, variables)

    return functionIR

def insertInstr_Statement(block, statementAST, variables):
    if isinstance(statementAST, ast.BlockStmt):
        insertInstr_Statement_Block(block, statementAST, variables)
    elif isinstance(statementAST, ast.AssignmentStmt):
        insertInstr_Statement_Assignment(block, statementAST, variables)
    elif isinstance(statementAST, ast.ReturnStmt):
        insertInstr_Statement_Return(block, statementAST, variables)
    elif isinstance(statementAST, ast.WhileStmt):
        insertInstr_Statement_While(block, statementAST, variables)
    elif isinstance(statementAST, ast.IfStmt):
        insertInstr_Statement_If(block, statementAST, variables)
    elif isinstance(statementAST, ast.IfElseStmt):
        insertInstr_Statement_IfElse(block, statementAST, variables)
    else:
        raise NotImplementedError(str(statementAST))

def insertInstr_Statement_Block(block, blockAST, variables):
    for statement in blockAST.statements:
        insertInstr_Statement(block, statement, variables)

def insertInstr_Statement_Assignment(block, assignmnentAST, variables):
    result = insertInstr_Expression(block, assignmnentAST.expression, variables)
    block.add(ir.MoveInstr(variables[assignmnentAST.target], result))

def insertInstr_Statement_Return(block, returnAST, variables):
    result = insertInstr_Expression(block, returnAST.expression, variables)
    block.add(ir.ReturnInstr(result))

def insertInstr_Statement_While(block, whileAST, variables):
    startLabel = block.newLabel("while_start")
    afterLabel = block.newLabel("while_after")
    block.add(startLabel)

    condResult = insertInstr_Expression(block, whileAST.condition, variables)
    block.add(ir.GotoIfZero(condResult, afterLabel))
    insertInstr_Statement(block, whileAST.statement, variables)
    block.add(ir.GotoInstr(startLabel))

    block.add(afterLabel)

def insertInstr_Statement_If(block, ifAST, variables):
    afterLabel = block.newLabel("if_after")
    condResult = insertInstr_Expression(block, ifAST.condition, variables)
    block.add(ir.GotoIfZero(condResult, afterLabel))
    insertInstr_Statement(block, ifAST.thenStatement, variables)
    block.add(afterLabel)

def insertInstr_Statement_IfElse(block, ifElseAST, variables):
    startElseLabel = block.newLabel("else_start")
    afterElseLabel = block.newLabel("else_end")

    condResult = insertInstr_Expression(block, ifElseAST.condition, variables)
    block.add(ir.GotoIfZero(condResult, startElseLabel))
    insertInstr_Statement(block, ifElseAST.thenStatement, variables)
    block.add(ir.GotoInstr(afterElseLabel))
    block.add(startElseLabel)
    insertInstr_Statement(block, ifElseAST.elseStatement, variables)
    block.add(afterElseLabel)

def insertInstr_Expression(block, expr, variables):
    if isinstance(expr, ast.ComparisonExpr):
        return insertInstr_Expression_Comparison(block, expr, variables)
    elif isinstance(expr, ast.AddSubExpr):
        return insertInstr_Expression_AddSub(block, expr, variables)
    elif isinstance(expr, ast.MulDivExpr):
        return insertInstr_Expression_MulDiv(block, expr, variables)
    elif isinstance(expr, ast.ConstInt):
        return insertInstr_Expression_ConstInt(block, expr)
    elif isinstance(expr, ast.Variable):
        return insertInstr_Expression_Variable(block, expr, variables)

def insertInstr_Expression_Comparison(block, expr, variables):
    result = ir.VirtualRegister()
    a = insertInstr_Expression(block, expr.left, variables)
    b = insertInstr_Expression(block, expr.right, variables)
    block.add(ir.CompareInstr(expr.operator, result, a, b))
    return result
        
def insertInstr_Expression_AddSub(block, expr, variables):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstr(result, 0))
    for term in expr.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = ir.TwoOpInstr(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_MulDiv(block, expr, variables):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstr(result, 1))
    for term in expr.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = ir.TwoOpInstr(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_ConstInt(block, intAST):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstr(result, intAST.value))
    return result
        
def insertInstr_Expression_Variable(block, variableAST, variables):
    return variables[variableAST.name]