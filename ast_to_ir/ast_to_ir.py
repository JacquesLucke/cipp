from cipp_parser.parser import (
    ProgramAST, AssignmentStmtAST, AddSubExprAST, ConstIntAST,
    VariableAST, MulDivExprAST, ReturnStmtAST, BlockStmtAST,
    WhileStmtAST
)
from ir_to_x64.ir import (
    ModuleIR, FunctionIR, VirtualRegister,
    InitializeInstrIR, TwoOpInstrIR, MoveInstrIR, ReturnInstrIR,
    GotoIfZeroIR, GotoInstrIR
)

def transformProgramToIR(programAST):
    functionsIRs = list(map(transformFunctionToIR, programAST.functions))
    return ModuleIR(functionsIRs)

def transformFunctionToIR(functionAST):
    functionIR = FunctionIR(functionAST.name)

    variables = {}
    for argument in functionAST.arguments:
        variables[argument.name] = functionIR.addArgument()

    insertInstr_Statement(functionIR.block, functionAST.statement, variables)

    return functionIR

def insertInstr_Statement(block, statementAST, variables):
    if isinstance(statementAST, BlockStmtAST):
        insertInstr_Statement_Block(block, statementAST, variables)
    elif isinstance(statementAST, AssignmentStmtAST):
        insertInstr_Statement_Assignment(block, statementAST, variables)
    elif isinstance(statementAST, ReturnStmtAST):
        insertInstr_Statement_Return(block, statementAST, variables)
    elif isinstance(statementAST, WhileStmtAST):
        insertInstr_Statement_While(block, statementAST, variables)

def insertInstr_Statement_Block(block, blockAST, variables):
    for statement in blockAST.statements:
        insertInstr_Statement(block, statement, variables)

def insertInstr_Statement_Assignment(block, assignmnentAST, variables):
    result = insertInstr_Expression(block, assignmnentAST.expression, variables)
    block.add(MoveInstrIR(variables[assignmnentAST.target], result))

def insertInstr_Statement_Return(block, returnAST, variables):
    result = insertInstr_Expression(block, returnAST.expression, variables)
    block.add(ReturnInstrIR(result))

def insertInstr_Statement_While(block, whileAST, variables):
    startLabel = block.newLabel("while_start")
    afterLabel = block.newLabel("while_after")
    block.add(startLabel)

    condResult = insertInstr_Expression(block, whileAST.condition, variables)
    block.add(GotoIfZeroIR(condResult, afterLabel))
    insertInstr_Statement(block, whileAST.statement, variables)
    block.add(GotoInstrIR(startLabel))

    block.add(afterLabel)

def insertInstr_Expression(block, expr, variables):
    if isinstance(expr, AddSubExprAST):
        return insertInstr_Expression_AddSub(block, expr, variables)
    elif isinstance(expr, MulDivExprAST):
        return insertInstr_Expression_MulDiv(block, expr, variables)
    elif isinstance(expr, ConstIntAST):
        return insertInstr_Expression_ConstInt(block, expr)
    elif isinstance(expr, VariableAST):
        return insertInstr_Expression_Variable(block, expr, variables)
        
def insertInstr_Expression_AddSub(block, expression, variables):
    result = VirtualRegister()
    block.add(InitializeInstrIR(result, 0))
    for term in expression.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_MulDiv(block, expression, variables):
    result = VirtualRegister()
    block.add(InitializeInstrIR(result, 1))
    for term in expression.terms:
        reg = insertInstr_Expression(block, term.expr, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        block.add(instr)
    return result

def insertInstr_Expression_ConstInt(block, intAST):
    result = VirtualRegister()
    block.add(InitializeInstrIR(result, intAST.value))
    return result
        
def insertInstr_Expression_Variable(block, variableAST, variables):
    return variables[variableAST.name]