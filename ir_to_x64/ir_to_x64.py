from x64assembler.instructions import (
    AddRegToRegInstr, MovImmToRegInstr, MovMemToRegInstr, MovRegToMemInstr,
    RetInstr, AddImmToRegInstr, SubRegFromRegInstr,
    JmpInstr, JmpZeroInstr, CompareInstr
)

from x64assembler.block import Block, Label
from x64assembler.registers import allRegisters

from . ir import (
    InitializeInstrIR, MoveInstrIR, ReturnInstrIR, TwoOpInstrIR,
    GotoInstrIR, GotoIfZeroIR,
    InstructionIR, LabelIR
)

globals().update(allRegisters)

def compileToX64(functionIR):
    elements = list(compileFunction(functionIR))
    block = Block(elements)
    return block

def compileFunction(functionIR):
    vregOffsets = {}
    for i, reg in enumerate(functionIR.getUsedVRegisters()):
        vregOffsets[reg] = i * 8

    yield from prepareStack(vregOffsets)

    for reg, vreg in zip([rcx, rdx, r8, r9], functionIR.arguments): # windows
    #for reg, vreg in zip([rdi, rsi, rdx, rcx, r8, r9], functionIR.arguments): # linux
        yield storeVirtualRegister(reg, vreg, vregOffsets)

    for irElement in functionIR.block:
        yield from elementToAssemblyElement(irElement, vregOffsets)

def elementToAssemblyElement(irElement, vregOffsets):
    if isinstance(irElement, InstructionIR):
        yield from irInstructionToAssembly(irElement, vregOffsets)
    elif isinstance(irElement, LabelIR):
        yield Label(irElement.name)

def irInstructionToAssembly(instr, vregOffsets):
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
    elif isinstance(instr, GotoInstrIR):
        yield JmpInstr(instr.label.name)
    elif isinstance(instr, GotoIfZeroIR):
        yield MovImmToRegInstr(rax, 0)
        yield loadVirtualRegister(rcx, instr.vreg, vregOffsets)
        yield CompareInstr(rax, rcx)
        yield JmpZeroInstr(instr.label.name)

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