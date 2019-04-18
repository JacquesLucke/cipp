from . import ir
from . x64assembler.block import Block, Label
from . x64assembler import instructions as x64
from . x64assembler.registers import allRegisters
from . platform_utils import onLinux, onWindows

globals().update(allRegisters)

def compileModule(moduleIR):
    elements = []
    for functionIR in moduleIR.functions:
        elements.append(Label(functionIR.name))
        elements.extend(compileFunction(functionIR))

    block = Block(elements)
    return block


# https://en.wikipedia.org/wiki/X86_calling_conventions#x86-64_calling_conventions
if onLinux:
    call_registers = [rdi, rsi, rdx, rcx, r8, r9]
elif onWindows:
    call_registers = [rcx, rdx, r8, r9]
else:
    raise Exception("unsupported platform")

def compileFunction(functionIR):
    vregOffsets = {}
    for i, reg in enumerate(functionIR.getUsedVRegisters()):
        vregOffsets[reg] = i * 8

    yield from prepareStack(vregOffsets)

    for reg, vreg in zip(call_registers, functionIR.arguments):
        yield storeVirtualRegister(reg, vreg, vregOffsets)

    for irElement in functionIR.block:
        yield from elementToAssemblyElement(irElement, vregOffsets)

def elementToAssemblyElement(irElement, vregOffsets):
    if isinstance(irElement, ir.Instruction):
        yield from irInstructionToAssembly(irElement, vregOffsets)
    elif isinstance(irElement, ir.Label):
        yield Label(irElement.name)

def irInstructionToAssembly(instr, vregOffsets):
    if isinstance(instr, ir.InitializeInstr):
        yield x64.MovImmToRegInstr(rax, instr.value)
        yield storeVirtualRegister(rax, instr.vreg, vregOffsets)
    elif isinstance(instr, ir.CompareInstr):
        yield loadVirtualRegister(rax, instr.a, vregOffsets)
        yield loadVirtualRegister(rcx, instr.b, vregOffsets)
        yield x64.CompareInstr(rax, rcx)
        yield x64.MovImmToRegInstr(rax, 0)
        yield {
            "!=" : x64.SetIfNotEqualInstr,
            "==" : x64.SetIfEqualInstr,
            ">" : x64.SetIfGreaterInstr,
            "<" : x64.SetIfLessInstr,
            ">=" : x64.SetIfGreaterOrEqualInstr,
            "<=" : x64.SetIfLessOrEqualInstr
        }[instr.operation](al)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    elif isinstance(instr, ir.MoveInstr):
        yield loadVirtualRegister(rax, instr.source, vregOffsets)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    elif isinstance(instr, ir.TwoOpInstr):
        yield loadVirtualRegister(rax, instr.a, vregOffsets)
        yield loadVirtualRegister(rcx, instr.b, vregOffsets)
        if instr.operation == "+":
            yield x64.AddRegToRegInstr(rax, rcx)
        elif instr.operation == "-":
            yield x64.SubRegFromRegInstr(rax, rcx)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    elif isinstance(instr, ir.ReturnInstr):
        yield loadVirtualRegister(rax, instr.vreg, vregOffsets)
        yield from clearStackAndReturn(vregOffsets)
    elif isinstance(instr, ir.GotoInstr):
        yield x64.JmpInstr(instr.label.name)
    elif isinstance(instr, ir.GotoIfZero):
        yield x64.MovImmToRegInstr(rax, 0)
        yield loadVirtualRegister(rcx, instr.vreg, vregOffsets)
        yield x64.CompareInstr(rax, rcx)
        yield x64.JmpZeroInstr(instr.label.name)
    elif isinstance(instr, ir.CallInstr):
        for vreg, reg in zip(instr.arguments, call_registers):
            yield loadVirtualRegister(reg, vreg, vregOffsets)
        yield x64.CallInstr(instr.label)
        yield storeVirtualRegister(rax, instr.target, vregOffsets)
    else:
        raise NotImplementedError(str(instr))

def changeStackPointer(byteAmount):
    return x64.AddImmToRegInstr(rsp, byteAmount)

def loadVirtualRegister(target, vreg, vregOffsets):
    return x64.MovMemToRegInstr(target, rsp, vregOffsets[vreg])

def storeVirtualRegister(source, vreg, vregOffsets):
    return x64.MovRegToMemInstr(rsp, source, vregOffsets[vreg])

def prepareStack(vregOffsets):
    yield changeStackPointer(-len(vregOffsets) * 8)

def clearStack(vregOffsets):
    yield changeStackPointer(len(vregOffsets) * 8)

def clearStackAndReturn(vregOffsets):
    yield from clearStack(vregOffsets)
    yield x64.RetInstr()
