from .. bits import Bits
from . instruction import Instruction

class MovRegToRegInstr(Instruction):
    def __init__(self, dstReg, srcReg):
        assert dstReg.size == srcReg.size

        self.regSize = dstReg.size
        self.dstReg = dstReg
        self.srcReg = srcReg

    def toIntelSyntax(self):
        return f"mov {self.dstReg.name}, {self.srcReg.name}"

    def toMachineCode(self):
        if self.regSize == 64:
            return self.toMachineCode_64()
        elif self.regSize == 32:
            return self.toMachineCode_32()
        elif self.regSize == 16:
            return self.toMachineCode_16()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        prefix = prefixesFor64BitMoves[(self.dstReg.group, self.srcReg.group)]
        return prefix + self.getBaseMachineCode()

    def toMachineCode_32(self):
        prefix = prefixesFor32BitMoves[(self.dstReg.group, self.srcReg.group)]
        return prefix + self.getBaseMachineCode()

    def toMachineCode_16(self):
        return Bits.fromHex("66") + self.toMachineCode_32()

    def getBaseMachineCode(self):
        opcode = Bits.fromHex("89")
        arguments = Bits("11") + self.srcReg.bits + self.dstReg.bits
        return opcode + arguments

prefixesFor64BitMoves = {
    (0, 0) : Bits.fromHex("48"),
    (1, 0) : Bits.fromHex("49"),
    (0, 1) : Bits.fromHex("4c"),
    (1, 1) : Bits.fromHex("4d")
}

prefixesFor32BitMoves = {
    (0, 0) : Bits.fromHex(""),
    (1, 0) : Bits.fromHex("41"),
    (0, 1) : Bits.fromHex("44"),
    (1, 1) : Bits.fromHex("45")
}
