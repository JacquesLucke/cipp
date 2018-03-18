from .. bits import Bits
from .. block import Instruction

class SetByteOnConditionInstr(Instruction):
    opcodeHex = NotImplemented
    intelSyntaxName = NotImplemented

    def __init__(self, reg):
        assert reg.size == 8
        self.reg = reg

    def toMachineCode(self):
        return Bits.fromHex(self.opcodeHex) + Bits("11000") + self.reg.bits

    def toIntelSyntax(self):
        return f"{self.intelSyntaxName} {self.reg.name}"

class SetIfNotEqualInstr(SetByteOnConditionInstr):
    opcodeHex = "0f95"
    intelSyntaxName = "setne"

class SetIfEqualInstr(SetByteOnConditionInstr):
    opcodeHex = "0f94"
    intelSyntaxName = "sete"

class SetIfGreaterInstr(SetByteOnConditionInstr):
    opcodeHex = "0f9f"
    intelSyntaxName = "setg"

class SetIfLessInstr(SetByteOnConditionInstr):
    opcodeHex = "0f9c"
    intelSyntaxName = "setl"