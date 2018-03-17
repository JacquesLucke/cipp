from x64assembler.instructions import (
    AddRegToRegInstr, MovImmToRegInstr, MovMemToRegInstr, MovRegToMemInstr,
    RetInstr, AddImmToRegInstr, SubRegFromRegInstr
)

from x64assembler.block import Block
from x64assembler.registers import allRegisters

from . ir import (
    InitializeInstrIR, MoveInstrIR, ReturnInstrIR, TwoOpInstrIR
)

globals().update(allRegisters)

def compileToX64(functionIR):
    instructions = list(compileFunction(functionIR))
    block = Block(instructions)
    return block

def compileFunction(functionIR):
    vregOffsets = {}
    for i, reg in enumerate(functionIR.getUsedVRegisters()):
        vregOffsets[reg] = i * 8

    yield from prepareStack(vregOffsets)

    for reg, vreg in zip([rcx, rdx, r8, r9], functionIR.arguments):
        yield storeVirtualRegister(reg, vreg, vregOffsets)

    for instr in functionIR.entryBlock.instructions:
        yield from compileInstruction(instr, vregOffsets)

def compileInstruction(instr, vregOffsets):
    if isinstance(instr, InitializeInstrIR):
        yield MovImmToRegInstr(rax, instr.value)
        yield storeVirtualRegister(rax, instr.vreg, vregOffsets)
    if isinstance(instr, MoveInstrIR):
        yield loadVirtualRegister(rax, instr.source, vregOffsets)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    elif isinstance(instr, TwoOpInstrIR):
        yield loadVirtualRegister(rax, instr.a, vregOffsets)
        yield loadVirtualRegister(rcx, instr.b, vregOffsets)
        if instr.operation == "+":
            yield AddRegToRegInstr(rax, rcx)
        elif instr.operation == "-":
            yield SubRegFromRegInstr(rax, rcx)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    elif isinstance(instr, ReturnInstrIR):
        yield loadVirtualRegister(rax, instr.vreg, vregOffsets)
        yield from clearStackAndReturn(vregOffsets)

def changeStackPointer(byteAmount):
    return AddImmToRegInstr(rsp, byteAmount)

def loadVirtualRegister(target, vreg, vregOffsets):
    return MovMemToRegInstr(target, rsp, vregOffsets[vreg])

def storeVirtualRegister(source, vreg, vregOffsets):
    return MovRegToMemInstr(rsp, source, vregOffsets[vreg])

def prepareStack(vregOffsets):
    yield changeStackPointer(-len(vregOffsets) * 8)

def clearStack(vregOffsets):
    yield changeStackPointer(len(vregOffsets) * 8)

def clearStackAndReturn(vregOffsets):
    yield from clearStack(vregOffsets)
    yield RetInstr()