from cipp_parser.parser import (
    ProgramAST, AssignmentStmtAST, AddSubExprAST, ConstIntAST,
    VariableAST, MulDivExprAST, ReturnStmtAST, BlockStmtAST
)
from ir_to_x64.ir import (
    ModuleIR, FunctionIR, VirtualRegister,
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

    instructions = []
    insertInstr_Statement(instructions, functionAST.statement, variables)

    for instr in instructions:
        functionIR.addInstruction(instr)

    return functionIR

def insertInstr_Statement(instructions, statementAST, variables):
    if isinstance(statementAST, BlockStmtAST):
        insertInstr_Statement_Block(instructions, statementAST, variables)
    elif isinstance(statementAST, AssignmentStmtAST):
        insertInstr_Statement_Assignment(instructions, statementAST, variables)
    elif isinstance(statementAST, ReturnStmtAST):
        insertInstr_Statement_Return(instructions, statementAST, variables)

def insertInstr_Statement_Block(instructions, blockAST, variables):
    for statement in blockAST.statements:
        insertInstr_Statement(instructions, statement, variables)

def insertInstr_Statement_Assignment(instructions, assignmnentAST, variables):
    result = insertInstr_Expression(instructions, assignmnentAST.expression, variables)
    instructions.append(MoveInstrIR(variables[assignmnentAST.target], result))

def insertInstr_Statement_Return(instructions, returnAST, variables):
    result = insertInstr_Expression(instructions, returnAST.expression, variables)
    instructions.append(ReturnInstrIR(result))

def insertInstr_Expression(instructions, expr, variables):
    if isinstance(expr, AddSubExprAST):
        return insertInstr_Expression_AddSub(instructions, expr, variables)
    elif isinstance(expr, MulDivExprAST):
        return insertInstr_Expression_MulDiv(instructions, expr, variables)
    elif isinstance(expr, ConstIntAST):
        return insertInstr_Expression_ConstInt(instructions, expr)
    elif isinstance(expr, VariableAST):
        return insertInstr_Expression_Variable(instructions, expr, variables)
        
def insertInstr_Expression_AddSub(instructions, expression, variables):
    result = VirtualRegister()
    instructions.append(InitializeInstrIR(result, 0))
    for term in expression.terms:
        reg = insertInstr_Expression(instructions, term.expr, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        instructions.append(instr)
    return result

def insertInstr_Expression_MulDiv(instructions, expression, variables):
    result = VirtualRegister()
    instructions.append(InitializeInstrIR(result, 1))
    for term in expression.terms:
        reg = insertInstr_Expression(instructions, term.expr, variables)
        instr = TwoOpInstrIR(term.operation, result, result, reg)
        instructions.append(instr)
    return result

def insertInstr_Expression_ConstInt(instructions, intAST):
    result = VirtualRegister()
    instructions.append(InitializeInstrIR(result, intAST.value))
    return result
        
def insertInstr_Expression_Variable(instructions, variableAST, variables):
    return variables[variableAST.name]