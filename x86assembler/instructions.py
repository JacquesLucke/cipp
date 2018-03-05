from . bits import Bits

class Instruction:
    def toMachineCode(self):
        raise NotImplementedError()

    def toIntelSyntax(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.toString()


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
        targetReg = self.target.bits
        addrReg = self.addrReg.bits
        if self.offset == 0:
            if addrReg == "100": # special case esp
                pass
            else:
                mod = Bits("00")
                immOffset = Bits("")
        elif -128 <= self.offset <= 127:
            mod = Bits("01")
            immOffset = Bits.fromInt(self.offset, length = 8)
        else:
            mod = Bits("10")
            immOffset = Bits.fromInt(self.offset, length = 32).reversedBytes()
        return Bits.join(opcode, mod, targetReg, addrReg, immOffset)

    def toIntelSyntax(self):
        if self.offset > 0:
            return f"mov {self.target.name}, [{self.addrReg.name} + {self.offset}]"
        elif self.offset < 0:
            return f"mov {self.target.name}, [{self.addrReg.name} - {abs(self.offset)}]"
        else:
            return f"mov {self.target.name}, [{self.addrReg.name}]"


def intFromHex(hexcode):
    return int(hexcode, base = 16)
