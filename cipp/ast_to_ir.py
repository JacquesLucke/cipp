from . import ir
from . import ast

def transformProgramToIR(programAST):
    functionsIRs = list(map(transformFunctionToIR, programAST.functions))
    return ir.ModuleIR(functionsIRs)

def transformFunctionToIR(functionAST):
    functionIR = ir.FunctionIR(functionAST.name)

    variables = {}
    for argument in functionAST.arguments:
        variables[argument.name] = functionIR.addArgument()

    insertInstr_Statement(functionIR.block, functionAST.statement, variables)

    return functionIR

def insertInstr_Statement(block, statementAST, variables):
    if isinstance(statementAST, ast.BlockStmtAST):
        insertInstr_Statement_Block(block, statementAST, variables)
    elif isinstance(statementAST, ast.AssignmentStmtAST):
        insertInstr_Statement_Assignment(block, statementAST, variables)
    elif isinstance(statementAST, ast.ReturnStmtAST):
        insertInstr_Statement_Return(block, statementAST, variables)
    elif isinstance(statementAST, ast.WhileStmtAST):
        insertInstr_Statement_While(block, statementAST, variables)
    elif isinstance(statementAST, ast.IfStmtAST):
        insertInstr_Statement_If(block, statementAST, variables)
    elif isinstance(statementAST, ast.IfElseStmtAST):
        insertInstr_Statement_IfElse(block, statementAST, variables)
    else:
        raise NotImplementedError(str(statementAST))

def insertInstr_Statement_Block(block, blockAST, variables):
    for statement in blockAST.statements:
        insertInstr_Statement(block, statement, variables)

def insertInstr_Statement_Assignment(block, assignmnentAST, variables):
    result = insertInstr_Expression(block, assignmnentAST.expression, variables)
    block.add(ir.MoveInstrIR(variables[assignmnentAST.target], result))

def insertInstr_Statement_Return(block, returnAST, variables):
    result = insertInstr_Expression(block, returnAST.expression, variables)
    block.add(ir.ReturnInstrIR(result))

def insertInstr_Statement_While(block, whileAST, variables):
    startLabel = block.newLabel("while_start")
    afterLabel = block.newLabel("while_after")
    block.add(startLabel)

    condResult = insertInstr_Expression(block, whileAST.condition, variables)
    block.add(ir.GotoIfZeroIR(condResult, afterLabel))
    insertInstr_Statement(block, whileAST.statement, variables)
    block.add(ir.GotoInstrIR(startLabel))

    block.add(afterLabel)

def insertInstr_Statement_If(block, ifAST, variables):
    afterLabel = block.newLabel("if_after")
    condResult = insertInstr_Expression(block, ifAST.condition, variables)
    block.add(ir.GotoIfZeroIR(condResult, afterLabel))
    insertInstr_Statement(block, ifAST.thenStatement, variables)
    block.add(afterLabel)

def insertInstr_Statement_IfElse(block, ifElseAST, variables):
    startElseLabel = block.newLabel("else_start")
    afterElseLabel = block.newLabel("else_end")

    condResult = insertInstr_Expression(block, ifElseAST.condition, variables)
    block.add(ir.GotoIfZeroIR(condResult, startElseLabel))
    insertInstr_Statement(block, ifElseAST.thenStatement, variables)
    block.add(ir.GotoInstrIR(afterElseLabel))
    block.add(startElseLabel)
    insertInstr_Statement(block, ifElseAST.elseStatement, variables)
    block.add(afterElseLabel)

def insertInstr_Expression(block, expr, variables):
    if isinstance(expr, ast.ComparisonExprAST):
        return insertInstr_Expression_Comparison(block, expr, variables)
    elif isinstance(expr, ast.AddSubExprAST):
        return insertInstr_Expression_AddSub(block, expr, variables)
    elif isinstance(expr, ast.MulDivExprAST):
        return insertInstr_Expression_MulDiv(block, expr, variables)
    elif isinstance(expr, ast.ConstIntAST):
        return insertInstr_Expression_ConstInt(block, expr)
    elif isinstance(expr, ast.VariableAST):
        return insertInstr_Expression_Variable(block, expr, variables)

def insertInstr_Expression_Comparison(block, expr, variables):
    result = ir.VirtualRegister()
    a = insertInstr_Expression(block, expr.left, variables)
    b = insertInstr_Expression(block, expr.right, variables)
    block.add(ir.CompareInstrIR(expr.operator, result, a, b))
    return result
        
def insertInstr_Expression_AddSub(block, expr, variables):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstrIR(result, 0))
    for term in expr.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = ir.TwoOpInstrIR(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_MulDiv(block, expr, variables):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstrIR(result, 1))
    for term in expr.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = ir.TwoOpInstrIR(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_ConstInt(block, intAST):
    result = ir.VirtualRegister()
    block.add(ir.InitializeInstrIR(result, intAST.value))
    return result
        
def insertInstr_Expression_Variable(block, variableAST, variables):
    return variables[variableAST.name]