from .. bits import Bits
from . utils import getImmSize
from . instruction import Instruction

class MovImmToRegInstr(Instruction):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

    def toMachineCode(self):
        if self.reg.size == 64:
            return self.toMachineCode_64()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        prefix = Bits.fromHex("48" if self.reg.group == 0 else "49")

        immSize = getImmSize(self.value)
        if immSize <= 4:
            opcode = Bits.fromHex("c7")
            arguments = Bits("11000") + self.reg.bits
            imm = self.getImmBits(length = 32)
            return Bits.join(prefix, opcode, arguments, imm)
        else:
            opcode = Bits.fromHexAndOffset("b8", self.reg.number)
            imm = self.getImmBits(length = 64)
            return Bits.join(prefix, opcode, imm)

    def getImmBits(self, length):
        return Bits.fromInt(self.value, length).reversedBytes()

    def toIntelSyntax(self):
        return f"mov {self.reg.name}, {self.value}"
