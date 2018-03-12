from .. bits import Bits
from . instruction import Instruction
from . utils import getRegGroupPrefix_64

class MovMemToRegInstr(Instruction):
    def __init__(self, dstReg, addrReg, offset = 0):
        if offset != 0:
            raise NotImplementedError()
        self.dstReg = dstReg
        self.addrReg = addrReg
        self.offset = offset

    def toMachineCode(self):
        if self.dstReg.size == 64:
            return self.toMachineCode_64()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        prefix = getRegGroupPrefix_64(self.addrReg, self.dstReg)
        opcode = Bits.fromHex("8b")
        if self.addrReg.number == 5: # special case for rbp and r13
            arguments = Bits("01") + self.dstReg.bits + self.addrReg.bits
            arguments += Bits.fromInt(0, length = 8)
        else:
            arguments = Bits("00") + self.dstReg.bits + self.addrReg.bits

        if self.addrReg.number == 4:
            arguments += Bits.fromHex("24")

        return Bits.join(prefix, opcode, arguments)

    def toIntelSyntax(self):
        if self.offset == 0:
            return f"mov {self.dstReg.name}, [{self.addrReg.name}]"
        else:
            return f"mov {self.dstReg.name}, [{self.addrReg.name} + {self.offset}]"
