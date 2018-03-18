from .. bits import Bits
from .. block import Instruction

class PushImmInstr(Instruction):
    def __init__(self, value):
        assert -2**31 <= value <= 2**32 - 1
        self.value = value

    def toMachineCode(self):
        if -128 <= self.value <= 127:
            opcode = Bits.fromHex("6a")
            imm = Bits.fromInt(self.value, length = 8)
        else:
            opcode = Bits.fromHex("68")
            imm = Bits.fromInt(self.value, length = 32).reversedBytes()
        return opcode + imm

    def toIntelSyntax(self):
        return f"push {self.value}"
