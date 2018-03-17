from . bits import Bits

class Block:
    def __init__(self, instructions = [], labels = {}):
        self.instructions = instructions
        self.labels = labels

    def toIntelSyntax(self):
        return "\n".join(instr.toIntelSyntax() for instr in self.instructions)

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
                if link.label not in self.labels:
                    raise Exception(f"cannot find label: {link.label}")

                linkedInstruction = self.labels[link.label]
                linkedPosition = positionByInstruction[linkedInstruction]
                offset = linkedPosition - positionOfNextInstr
                machineCode = link.insertOffset(machineCode, offset)
            
            resultParts.append(machineCode)
        
        return Bits.join(*resultParts)