from array import array
from exec_utils import createFunctionFromHex

from x64assembler.block import Block
from x64assembler.registers import allRegisters
from x64assembler.instructions import (
    AddImmToRegInstr, MovRegToRegInstr, RetInstr, 
    PushRegInstr, PopRegInstr, SyscallInstr, 
    MovImmToRegInstr, PushImmInstr, AddRegToRegInstr,
    MovMemToRegInstr, MovRegToMemInstr
)

globals().update(allRegisters)

N = 10000
def genInstructions():
    for i in range(N):
        yield MovMemToRegInstr(rax, rdi)
        yield AddImmToRegInstr(rax, 1)
        yield MovRegToMemInstr(rdi, rax)
        yield AddImmToRegInstr(rdi, 8)
    yield RetInstr()

instructions = list(genInstructions())
block = Block(instructions)
#print(block.toIntelSyntax())

from ctypes import c_void_p, CFUNCTYPE
functype = CFUNCTYPE(None, c_void_p)
func1 = createFunctionFromHex(functype, Block(instructions).toMachineCode().toHex())

def func2(numbers):
    for i in range(len(numbers)):
        numbers[i] += 1

from timeit import timeit

import numpy as np
arr = np.zeros(N, np.int64)

repetitions = 1000
res1 = timeit("func1(arr.ctypes.data)", globals = globals(), number = repetitions)
res2 = timeit("func2(arr)", globals = globals(), number = repetitions)

print(res2 / res1)