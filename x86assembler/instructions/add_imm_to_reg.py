from .. bits import Bits
from .. registers import rax, eax, ax
from . instruction import Instruction

class AddImmToRegInstr(Instruction):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

    def toIntelSyntax(self):
        return f"add {self.reg.name}, {self.value}"

    def toMachineCode(self):
        if self.reg.size == 64:
            return self.toMachineCode_64()
        elif self.reg.size == 32:
            return self.toMachineCode_32()
        elif self.reg.size == 16:
            return self.toMachineCode_16()
        else:
            raise NotImplementedError()

    def toMachineCode_64(self):
        prefix = Bits.fromHex("48" if self.reg.group == 0 else "49")
        return prefix + self.getBaseMachineCode()

    def toMachineCode_32(self):
        prefix = Bits.fromHex("" if self.reg.group == 0 else "41")
        return prefix + self.getBaseMachineCode()

    def toMachineCode_16(self):
        prefix = Bits.fromHex("" if self.reg.group == 0 else "41")
        return Bits.fromHex("66") + prefix + self.getBaseMachineCode(allow16Bit = True)

    def getBaseMachineCode(self, allow16Bit = False):
        immSize = getImmSize(self.value)
        if immSize <= 1:
            opcode = Bits.fromHex("83")
            arguments = Bits("11000") + self.reg.bits
            imm = self.getImmBits(length = 8)
        elif immSize in (2, 4):
            imm = self.getImmBits(length = 32 if not allow16Bit else 16)
            if self.reg in (rax, eax, ax):
                opcode = Bits.fromHex("05")
                arguments = Bits("")
            else:
                opcode = Bits.fromHex("81")
                arguments = Bits("11000") + self.reg.bits
        else:
            raise NotImplementedError()
        return Bits.join(opcode, arguments, imm)

    def getImmBits(self, length):
        return Bits.fromInt(self.value, length).reversedBytes()

def getImmSize(n):
    if n == 0:
        return 0
    elif -2**7 <= n <= 2**7 - 1:
        return 1
    elif -2**15 <= n <= 2**15 - 1:
        return 2
    else:
        return 4
