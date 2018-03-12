from .. bits import Bits
from . instruction import Instruction
from . utils import getRegGroupPrefix_64

class MovRegToMemInstr(Instruction):
    def __init__(self, addrReg, srcReg, offset = 0):
        if offset != 0:
            raise NotImplementedError()
        self.addrReg = addrReg
        self.srcReg = srcReg
        self.offset = offset

    def toMachineCode(self):
        if self.srcReg.size == 64:
            return self.toMachineCode_64()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        prefix = getRegGroupPrefix_64(self.addrReg, self.srcReg)
        opcode = Bits.fromHex("89")
        if self.addrReg.number == 5: # special case for rbp and r13
            arguments = Bits("01") + self.srcReg.bits + self.addrReg.bits
            arguments += Bits.fromInt(0, length = 8)
        else:
            arguments = Bits("00") + self.srcReg.bits + self.addrReg.bits

        if self.addrReg.number == 4:
            arguments += Bits.fromHex("24")

        return Bits.join(prefix, opcode, arguments)

    def toIntelSyntax(self):
        if self.offset == 0:
            return f"mov [{self.addrReg.name}], {self.srcReg.name}"
        else:
            return f"mov [{self.addrReg.name} + {self.offset}], {self.srcReg.name}"
