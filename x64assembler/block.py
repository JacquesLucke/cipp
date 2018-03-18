from . bits import Bits

class AssemblyElement:
    def toIntelSyntax(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.toIntelSyntax()

class Label(AssemblyElement):
    def __init__(self, name):
        self.name = name

    def toIntelSyntax(self):
        return f"{self.name}:"

    def __repr__(self):
        return f"<Label: {self.name}>"

class Instruction(AssemblyElement):
    def toMachineCode(self):
        raise NotImplementedError()

    def getLinks(self):
        return []

class Block:
    def __init__(self, elements):
        self.elements = elements

    def toIntelSyntax(self):
        return "\n".join(self._iterIntelSyntaxLines())

    def _iterIntelSyntaxLines(self):
        for element in self.elements:
            yield element.toIntelSyntax()

    def toMachineCode(self):
        position = 0
        positionByLabel = {}
        machineCodes = []

        for element in self.elements:
            if isinstance(element, Label):
                label = element.name
                if label in positionByLabel:
                    raise Exception(f"Label found twice: {label}")
                else:
                    positionByLabel[element.name] = position
            elif isinstance(element, Instruction):
                machineCode = element.toMachineCode()
                machineCodes.append((element, position, machineCode))
                position += machineCode.byteLength

        resultParts = []

        for instruction, ownPosition, machineCode in machineCodes:
            positionOfNextInstr = ownPosition + machineCode.byteLength

            for link in instruction.getLinks():
                if link.label not in positionByLabel:
                    raise Exception(f"cannot find label: {link.label}")

                linkedPosition = positionByLabel[link.label]
                offset = linkedPosition - positionOfNextInstr
                machineCode = link.insertOffset(machineCode, offset)
            
            resultParts.append(machineCode)
        
        return Bits.join(*resultParts)