from .. bits import Bits
from . instruction import Instruction

class PopRegInstr(Instruction):
    def __init__(self, reg):
        assert reg.size in (16, 64)
        self.reg = reg

    def toIntelSyntax(self):
        return f"pop {self.reg.name}"

    def toMachineCode(self):
        if self.reg.size == 64:
            return self.toMachineCode_64()
        elif self.reg.size == 16:
            return self.toMachineCode_16()
        else:
            raise Exception()

    def toMachineCode_64(self):
        prefix = Bits.fromHex("" if self.reg.group == 0 else "41")
        opcodeInt = int("58", base = 16) + self.reg.number
        opcode = Bits.fromInt(opcodeInt, length = 8)
        return prefix + opcode

    def toMachineCode_16(self):
        return Bits.fromHex("66") + self.toMachineCode_64()
