from .. bits import Bits
from .. block import Instruction

class RetInstr(Instruction):
    def __new__(self, popAmount = 0):
        if popAmount == 0:
            return RetnNoImmInstr()
        else:
            return RetnImmInstr(popAmount)

class RetnImmInstr(Instruction):
    def __init__(self, popAmount):
        assert 0 <= popAmount <= 2**16 - 1
        self.popAmount = popAmount

    def toMachineCode(self):
        imm = Bits.fromInt(self.popAmount, length = 16).reversedBytes()
        return Bits.fromHex("C2") + imm

    def toIntelSyntax(self):
        return f"ret {self.popAmount}"

class RetnNoImmInstr(Instruction):
    def toMachineCode(self):
        return Bits.fromHex("C3")

    def toIntelSyntax(self):
        return "ret"
