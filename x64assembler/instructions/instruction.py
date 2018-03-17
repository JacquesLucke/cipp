from .. bits import Bits

class Instruction:
    def toMachineCode(self):
        raise NotImplementedError()

    def toIntelSyntax(self):
        raise NotImplementedError()

    def getLinks(self):
        return []

    def __repr__(self):
        return self.toIntelSyntax()
