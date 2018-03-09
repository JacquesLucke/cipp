from .. bits import Bits

class Instruction:
    def toMachineCode(self):
        raise NotImplementedError()

    def toIntelSyntax(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.toIntelSyntax()


class RetInstr(Instruction):
    def toMachineCode(self):
        return Bits.fromHex("C3")

    def toIntelSyntax(self):
        return "ret"

class SingleRegBaseInstruction(Instruction):
    baseOpcodeHex = NotImplemented
    intelSyntaxName = NotImplemented

    def __init__(self, reg):
        self.reg = reg

    def toMachineCode(self):
        return Bits.fromInt(intFromHex(self.baseOpcodeHex) + self.reg.number, length = 8)

    def toIntelSyntax(self):
        return f"{self.intelSyntaxName} {self.reg.name}"

class PushInstr(SingleRegBaseInstruction):
    baseOpcodeHex = "50"
    intelSyntaxName = "push"

class PopInstr(SingleRegBaseInstruction):
    baseOpcodeHex = "58"
    intelSyntaxName = "pop"

class IncInstr(SingleRegBaseInstruction):
    baseOpcodeHex = "40"
    intelSyntaxName = "inc"

class DecInstr(SingleRegBaseInstruction):
    baseOpcodeHex = "48"
    intelSyntaxName = "dec"

class RegToRegBaseInstruction(Instruction):
    opcodeHex = NotImplemented
    intelSyntaxName = NotImplemented

    def __init__(self, target, source):
        self.target = target
        self.source = source

    def toMachineCode(self):
        opcode = Bits.fromHex(self.opcodeHex)
        mod = Bits("11") # indicates that the R/M field is also register
        return Bits.join(opcode, mod, self.source.bits, self.target.bits)

    def toIntelSyntax(self):
        return f"{self.intelSyntaxName} {self.target.name}, {self.source.name}"

class AddRegToRegInstr(RegToRegBaseInstruction):
    opcodeHex = "01"
    intelSyntaxName = "add"

class MovRegToRegInstr(RegToRegBaseInstruction):
    opcodeHex = "89"
    intelSyntaxName = "mov"

class MovImmToRegInstr(Instruction):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

    def toMachineCode(self):
        opcode = Bits.fromInt(intFromHex("B8") + self.reg.number, length = 8)
        imm = Bits.fromInt(self.value, length = 32).reversedBytes()
        return opcode + imm

    def toIntelSyntax(self):
        return f"mov {self.reg.name}, {self.value}"

class MovMemOffsetToRegInstr(Instruction):
    def __init__(self, target, addrReg, offset):
        self.target = target
        self.addrReg = addrReg
        self.offset = offset

    def toMachineCode(self):
        opcode = Bits.fromHex("8B")
        immOffset = Bits.fromInt(self.offset, length = 32).reversedBytes()
        if self.addrReg.bits == "100":
            return Bits.join(Bits.fromHex("8B8424"), immOffset)
        else:
            targetReg = self.target.bits
            addrReg = self.addrReg.bits
            mod = Bits("10")
            return Bits.join(opcode, mod, targetReg, addrReg, immOffset)

    def toIntelSyntax(self):
        if self.offset > 0:
            return f"mov {self.target.name}, [{self.addrReg.name} + {self.offset}]"
        elif self.offset < 0:
            return f"mov {self.target.name}, [{self.addrReg.name} - {abs(self.offset)}]"
        else:
            return f"mov {self.target.name}, [{self.addrReg.name}]"

class AddImmToRegInstr(Instruction):
    def __init__(self, reg, imm):
        self.reg = reg
        self.imm = imm

    def toMachineCode(self):
        opcode = Bits.fromHex("81")
        mod = Bits("11")
        reg = Bits("000")
        rm = self.reg.bits
        imm = Bits.fromInt(self.imm, length = 32).reversedBytes()
        return Bits.join(opcode, mod, reg, rm, imm)

    def toIntelSyntax(self):
        return f"add {self.reg.name}, {self.imm}"


def intFromHex(hexcode):
    return int(hexcode, base = 16)

def getMinImmSize(n):
    if n == 0:
        return 0
    elif -2**7 <= n <= 2**7 - 1:
        return 1
    elif -2**15 <= n <= 2**15 - 1:
        return 2
    else:
        return 4
