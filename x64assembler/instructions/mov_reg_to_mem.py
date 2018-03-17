from .. bits import Bits
from . instruction import Instruction
from . utils import getRegGroupPrefix_64, isTwosComplement

class MovRegToMemInstr(Instruction):
    def __init__(self, addrReg, srcReg, offset = 0):
        self.addrReg = addrReg
        self.srcReg = srcReg
        self.offset = offset

    def toMachineCode(self):
        if self.srcReg.size == 64:
            return self.toMachineCode_64()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        # The registers with number 4 (rsp, r12) and 5 (rbp, r13) have special cases.
        
        prefix = getRegGroupPrefix_64(self.addrReg, self.srcReg)
        opcode = Bits.fromHex("89")

        if self.offset == 0 and self.addrReg.number != 5:
            modBits = Bits("00")
            imm = Bits("")
        elif isTwosComplement(self.offset, 8):
            modBits = Bits("01")
            imm = Bits.fromInt(self.offset, length = 8)
        elif isTwosComplement(self.offset, 32):
            modBits = Bits("10")
            imm = Bits.fromInt(self.offset, length = 32).reversedBytes()
        else:
            raise NotImplementedError()

        arguments = modBits + self.srcReg.bits + self.addrReg.bits
        if self.addrReg.number == 4:
            arguments += Bits.fromHex("24")

        return Bits.join(prefix, opcode, arguments, imm)

    def toIntelSyntax(self):
        if self.offset == 0:
            return f"mov [{self.addrReg.name}], {self.srcReg.name}"
        elif self.offset < 0:
            return f"mov [{self.addrReg.name}{self.offset}], {self.srcReg.name}"
        else:
            return f"mov [{self.addrReg.name}+{self.offset}], {self.srcReg.name}"