from .. bits import Bits
from . instruction import Instruction

class JmpInstr(Instruction):
    def __init__(self, label):
        self.label = label

    def toMachineCode(self):
        return Bits.fromHex("e9") + Bits.zeros(32)

    def toIntelSyntax(self):
        return f"jmp {self.label}"

    def getLinks(self):
        return [JumpRelative32(self.label, startByte = 1)]

class JmpNotZeroInstr(Instruction):
    def __init__(self, label):
        self.label = label

    def toMachineCode(self):
        return Bits.fromHex("0f85") + Bits.zeros(32)

    def toIntelSyntax(self):
        return f"jnz {self.label}"

    def getLinks(self):
        return [JumpRelative32(self.label, startByte = 2)]

class JmpZeroInstr(Instruction):
    def __init__(self, label):
        self.label = label

    def toMachineCode(self):
        return Bits.fromHex("0f84") + Bits.zeros(32)

    def toIntelSyntax(self):
        return f"jz {self.label}"

    def getLinks(self):
        return [JumpRelative32(self.label, startByte = 2)]

class JumpRelative32:
    def __init__(self, label, startByte):
        self.label = label
        self.startByte = startByte

    def insertOffset(self, machineCode, offset):
        prefix = machineCode[:self.startByte * 8]
        suffix = machineCode[self.startByte * 8 + 32:]
        offsetBits = Bits.fromInt(offset, length = 32).reversedBytes()
        return prefix + offsetBits + suffix