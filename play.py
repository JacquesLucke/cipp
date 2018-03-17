import sys
from array import array
from exec_utils import createFunctionFromHex

from x64assembler.block import Block
from x64assembler.registers import allRegisters
from x64assembler.instructions import (
    AddImmToRegInstr, MovRegToRegInstr, RetInstr, 
    PushRegInstr, PopRegInstr, SyscallInstr, 
    MovImmToRegInstr, PushImmInstr, AddRegToRegInstr, JmpInstr
)

globals().update(allRegisters)

'''
Yes
89 101 115 10

01011001 01100101 01110011 00001010
'''

instructions1 = [
    MovImmToRegInstr(rcx, 0x0a736559),
    PushRegInstr(rcx), # write 'Yes' to stack

    MovImmToRegInstr(rax, 1), # use write syscall
    MovImmToRegInstr(rdi, 1), # write to stdout
    MovRegToRegInstr(rsi, rsp), # write what is on the stack
    MovImmToRegInstr(rdx, 4), # amount of symbols
    SyscallInstr(),

    PopRegInstr(rcx),
    MovImmToRegInstr(rax, 123),
    RetInstr()
]

'''
calling conventions:
    linux:
        return: rax
        arguments: rdi, rsi, rdx, rcx, r8, r9
        don't change: rbx, rbp, r12, r13, r14, r15
    windows:
        return: rax
        arguments: rcx, rdx, r8, r9
        don't change: rbx, rbp, rdi, rsi, rsp, r12, r13, r14, r15
'''

instructions2 = [
    MovImmToRegInstr(rax, 0),
    AddRegToRegInstr(rax, rcx),
    AddRegToRegInstr(rax, rdx),
    AddRegToRegInstr(rax, r8),
    RetInstr()
]

instructions3 = [
    MovImmToRegInstr(rax, 50),
    AddImmToRegInstr(rax, 50),
    RetInstr()
]

instructions4 = [
    JmpInstr("Case 1"),
    MovImmToRegInstr(rax, 10),
    JmpInstr("End"),
    MovImmToRegInstr(rax, 20),
    JmpInstr("End"),
    AddImmToRegInstr(rax, 5),
    AddImmToRegInstr(rax, 6),
    RetInstr()
]
labels4 = {
    "Case 1" : instructions4[1],
    "Case 2" : instructions4[3],
    "End" : instructions4[6]
}

block = Block(instructions4, labels4)
print(block.toIntelSyntax())
print(block.toMachineCode())
print(block.toMachineCode().toCArrayInitializer())

# sys.exit()

from ctypes import c_int, CFUNCTYPE
functype = CFUNCTYPE(c_int)
func = createFunctionFromHex(functype, block.toMachineCode().toHex())
result = func()
print(result)