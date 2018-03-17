from . bits import Bits

class Block:
    def __init__(self, instructions = [], labels = {}):
        self.instructions = instructions
        self.instructionByLabel = labels
        self.labelByInstruction = {instr : label for label, instr in labels.items()}

    def toIntelSyntax(self):
        return "\n".join(self._iterIntelSyntaxLines())

    def _iterIntelSyntaxLines(self):
        for instr in self.instructions:
            if instr in self.labelByInstruction:
                yield f"{self.labelByInstruction[instr]}:"
            yield str(instr)

    def toMachineCode(self):
        position = 0
        positionByInstruction = {}
        machineCodes = []

        for instruction in self.instructions:
            positionByInstruction[instruction] = position
            machineCode = instruction.toMachineCode()
            machineCodes.append(machineCode)
            position += machineCode.byteLength

        resultParts = []

        for instruction, machineCode in zip(self.instructions, machineCodes):
            positionOfNextInstr = positionByInstruction[instruction] + machineCode.byteLength

            for link in instruction.getLinks():
                if link.label not in self.instructionByLabel:
                    raise Exception(f"cannot find label: {link.label}")

                linkedInstruction = self.instructionByLabel[link.label]
                linkedPosition = positionByInstruction[linkedInstruction]
                offset = linkedPosition - positionOfNextInstr
                machineCode = link.insertOffset(machineCode, offset)
            
            resultParts.append(machineCode)
        
        return Bits.join(*resultParts)