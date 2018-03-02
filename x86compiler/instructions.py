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
        return Bits.fromPosInt(intFromHex(self.baseOpcodeHex) + self.reg.number, length = 8)

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

class MovImmInstr(Instruction):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

    def toMachineCode(self):
        opcode = Bits.fromPosInt(intFromHex("B8") + self.reg.number, length = 8)
        imm = Bits.fromPosInt(self.value, length = 32).reversedBytes()
        return opcode + imm

    def toIntelSyntax(self):
        return f"mov {self.reg.name}, {self.value}"

def intFromHex(hexcode):
    return int(hexcode, base = 16)
