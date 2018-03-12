from array import array
from exec_utils import createFunctionFromHex

from x64assembler.block import Block
from x64assembler.registers import allRegisters
from x64assembler.instructions import (
    AddImmToRegInstr, MovRegToRegInstr, RetInstr, 
    PushRegInstr, PopRegInstr, SyscallInstr, 
    MovImmToRegInstr, PushImmInstr, AddRegToRegInstr
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
calling convention (on linux):
arguments: rdi, rsi, rdx, rcx, r8, r9
don't change: rbx, rbp, r12, r13, r14, r15
'''

instructions2 = [
    MovImmToRegInstr(rax, 0),
    AddRegToRegInstr(rax, rdi),
    AddRegToRegInstr(rax, rsi),
    AddRegToRegInstr(rax, rdx),
    RetInstr()
]

block = Block(instructions2)
print(block.toIntelSyntax())
print(block.toMachineCode())

from ctypes import c_int, CFUNCTYPE
functype = CFUNCTYPE(c_int, c_int, c_int, c_int)
func = createFunctionFromHex(functype, block.toMachineCode().toHex())
result = func(32, 45, 3)
print(result)