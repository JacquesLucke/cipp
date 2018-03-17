from cipp_parser.parser import (
    ProgramAST, AssignmentStmtAST, AddSubExprAST, ConstIntAST,
    VariableAST, MulDivExprAST, ReturnStmtAST, BlockStmtAST
)
from ir_to_x64.ir import (
    ModuleIR, FunctionIR, BlockIR, VirtualRegister,
    InitializeInstrIR, TwoOpInstrIR, MoveInstrIR, ReturnInstrIR
)

def transformProgramToIR(programAST):
    functionsIRs = list(map(transformFunctionToIR, programAST.functions))
    return ModuleIR(functionsIRs)

def transformFunctionToIR(functionAST):
    functionIR = FunctionIR(functionAST.name)

    variables = {}
    for argument in functionAST.arguments:
        variables[argument.name] = functionIR.addArgument()

    entry = functionIR.entryBlock
    transformStatementToIR(functionAST.statement, entry, variables)
    print(entry)
    return functionIR

def transformStatementToIR(statementAST, block, variables):
    if isinstance(statementAST, BlockStmtAST):
        transformStatementToIR_Block(statementAST, block, variables)
    elif isinstance(statementAST, AssignmentStmtAST):
        transformStatementToIR_Assignment(statementAST, block, variables)
    elif isinstance(statementAST, ReturnStmtAST):
        transformStatementToIR_Return(statementAST, block, variables)

def transformStatementToIR_Block(blockAST, block, variables):
    for statement in blockAST.statements:
        transformStatementToIR(statement, block, variables)

def transformStatementToIR_Assignment(assignmnentAST, block, variables):
    result = transformExpressionToIR(assignmnentAST.expression, block, variables)
    block.append(MoveInstrIR(variables[assignmnentAST.target], result))

def transformStatementToIR_Return(returnAST, block, variables):
    result = transformExpressionToIR(returnAST.expression, block, variables)
    block.append(ReturnInstrIR(result))

def transformExpressionToIR(expr, block, variables):
    if isinstance(expr, AddSubExprAST):
        return transformExpressionToIR_AddSub(expr, block, variables)
    elif isinstance(expr, MulDivExprAST):
        return transformExpressionToIR_MulDiv(expr, block, variables)
    elif isinstance(expr, ConstIntAST):
        return transformExpressionToIR_ConstInt(expr, block)
    elif isinstance(expr, VariableAST):
        return transformExpressionToIR_Variable(expr, block, variables)
        
def transformExpressionToIR_AddSub(expression, block, variables):
    result = VirtualRegister()
    block.append(InitializeInstrIR(result, 0))
    for term in expression.terms:
        reg = transformExpressionToIR(term.expr, block, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        block.append(instr)
    return result

def transformExpressionToIR_MulDiv(expression, block, variables):
    result = VirtualRegister()
    block.append(InitializeInstrIR(result, 1))
    for term in expression.terms:
        reg = transformExpressionToIR(term.expr, block, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        block.append(instr)
    return result

def transformExpressionToIR_ConstInt(intAST, block):
    result = VirtualRegister()
    block.append(InitializeInstrIR(result, intAST.value))
    return result
        
def transformExpressionToIR_Variable(variableAST, block, variables):
    return variables[variableAST.name]