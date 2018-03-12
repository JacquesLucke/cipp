from array import array
from exec_utils import createFunctionFromHex

from x86assembler.block import Block
from x86assembler.registers import allRegisters
from x86assembler.instructions import AddImmToRegInstr, MovRegToRegInstr, RetInstr, PushRegInstr, PopRegInstr, SyscallInstr, MovImmToRegInstr, PushImmInstr

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

instructions2 = [
    MovImmToRegInstr(rax, 42),
    RetInstr()
]

block = Block(instructions1)
print(block.toIntelSyntax())
print(block.toMachineCode())

from ctypes import c_int, CFUNCTYPE
functype = CFUNCTYPE(c_int, c_int)
func = createFunctionFromHex(functype, block.toMachineCode().toHex())
result = func(0)
print(result)