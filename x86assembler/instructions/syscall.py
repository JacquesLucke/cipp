from .. bits import Bits
from . instruction import Instruction

class SyscallInstr(Instruction):
    def toIntelSyntax(self):
        return "syscall"

    def toMachineCode(self):
        return Bits.fromHex("0F05")
