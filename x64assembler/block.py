from . bits import Bits

class Block:
    def __init__(self, instructions = []):
        self.instructions = instructions

    def append(self, instruction):
        self.instructions.append(instruction)

    def toIntelSyntax(self):
        return "\n".join(instr.toIntelSyntax() for instr in self.instructions)

    def toMachineCode(self):
        return Bits.join(*[instr.toMachineCode() for instr in self.instructions])
