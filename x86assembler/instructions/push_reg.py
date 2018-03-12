from .. bits import Bits
from . instruction import Instruction

class PushRegInstr(Instruction):
    def __init__(self, reg):
        assert reg.size in (16, 64)
        self.reg = reg

    def toIntelSyntax(self):
        return f"push {self.reg.name}"

    def toMachineCode(self):
        if self.reg.size == 64:
            return self.toMachineCode_64()
        elif self.reg.size == 16:
            return self.toMachineCode_16()
        else:
            raise Exception()

    def toMachineCode_64(self):
        prefix = Bits.fromHex("" if self.reg.group == 0 else "41")
        opcode = Bits.fromHexAndOffset("50", self.reg.number)
        return prefix + opcode

    def toMachineCode_16(self):
        return Bits.fromHex("66") + self.toMachineCode_64()
