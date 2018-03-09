from array import array

from x86assembler.block import Block
from x86assembler.registers import allRegisters
from x86assembler.instructions import AddImmToRegInstr, MovRegToRegInstr, RetInstr, PushRegInstr, PopRegInstr, SyscallInstr

globals().update(allRegisters)

'''
Yes
89 101 115

01011001 01100101 01110011
'''

instructions = [
    MovRegToRegInstr(rcx, rdi),
    AddImmToRegInstr(rcx, 7562585),
    PushRegInstr(rcx), # write 'Yes' to stack

    MovRegToRegInstr(rax, rdi),
    MovRegToRegInstr(rsi, rdi),
    MovRegToRegInstr(rdx, rdi),

    AddImmToRegInstr(rax, 1), # use write syscall
    AddImmToRegInstr(rdi, 1), # write to stdout
    MovRegToRegInstr(rsi, rsp), # write what is on the stack
    AddImmToRegInstr(rsi, 0), # (optionally move write start)
    AddImmToRegInstr(rdx, 3), # write 3 symbols
    SyscallInstr(),

    PopRegInstr(rcx),
    RetInstr()
]

block = Block(instructions)
print(block.toIntelSyntax())
print(block.toMachineCode())

hexCode = block.toMachineCode().toHex()
arr = array("B", bytearray.fromhex(hexCode))
arrPointer = arr.buffer_info()[0]

from ctypes import cdll, c_int, c_void_p, memmove, CFUNCTYPE
libc = cdll.LoadLibrary("libc.so.6")
libc.valloc.argtypes = [c_int]
libc.restype = c_void_p

def allocateExecutableMemory(size):
    PROT_READ = 1
    PROT_WRITE = 2
    PROT_EXEC = 4

    p = libc.valloc(size)
    libc.mprotect(p, size, PROT_READ | PROT_WRITE | PROT_EXEC)
    return p


bufferPointer = allocateExecutableMemory(len(arr))
memmove(bufferPointer, arrPointer, len(arr))

functype = CFUNCTYPE(c_int, c_int)
func = functype(bufferPointer)
func(0)
