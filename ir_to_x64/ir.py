class ModuleIR:
    def __init__(self, functions):
        self.functions = functions

class FunctionIR:
    def __init__(self, name):
        self.name = name
        self.arguments = []
        self.block = CodeBlockIR()

    def addArgument(self):
        reg = VirtualRegister()
        self.arguments.append(reg)
        return reg
    
    def getUsedVRegisters(self):
        registers = set()
        registers.update(self.arguments)
        registers.update(self.block.iterUsedVRegisters())
        return registers

    def __repr__(self):
        return f"{self.name} ({', '.join(map(str, self.arguments))})\n{self.block}"

class CodeBlockIR:
    def __init__(self):
        self.elements = []
        self.usedLabels = set()

    def add(self, element):
        self.elements.append(element)

    def newLabel(self, prefix):
        i = 0
        while True:
            i += 1
            label = f"{prefix}_{i}"
            if label not in self.usedLabels:
                break
        self.usedLabels.add(label)
        return LabelIR(label)

    def iterUsedVRegisters(self):
        for element in self.elements:
            if isinstance(element, InstructionIR):
                yield from element.getVRegisters()

    def __iter__(self):
        return iter(self.elements)

    def __repr__(self):
        return "\n".join(self._iterReprLines())

    def _iterReprLines(self):
        for element in self.elements:
            if isinstance(element, InstructionIR):
                yield str(element)
            elif isinstance(element, LabelIR):
                yield f"{element.name}:"

class LabelIR:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f"<IR Label: {self.name}>"
    

class InstructionIR:
    def getVRegisters(self):
        return []

class TwoOpInstrIR(InstructionIR):
    def __init__(self, operation, target, a, b):
        self.operation = operation
        self.target = target
        self.a = a
        self.b = b

    def getVRegisters(self):
        return [self.target, self.a, self.b]

    def __repr__(self):
        return f"{self.target} = {self.a} {self.operation} {self.b}"

class InitializeInstrIR(InstructionIR):
    def __init__(self, vreg, value):
        self.vreg = vreg
        self.value = value

    def getVRegisters(self):
        return [self.vreg]

    def __repr__(self):
        return f"{self.vreg} = {self.value}"

class MoveInstrIR(InstructionIR):
    def __init__(self, target, source):
        self.target = target
        self.source = source

    def getVRegisters(self):
        return [self.target, self.source]

    def __repr__(self):
        return f"{self.target} = {self.source}"

class ReturnInstrIR(InstructionIR):
    def __init__(self, vreg = None):
        self.vreg = vreg

    def getVRegisters(self):
        return [self.vreg]

    def __repr__(self):
        return f"return {self.vreg}"

class GotoInstrIR(InstructionIR):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"goto {self.label.name}"

class GotoIfZeroIR(InstructionIR):
    def __init__(self, vreg, label):
        self.vreg = vreg
        self.label = label

    def getVRegisters(self):
        return [self.vreg]

    def __repr__(self):
        return f"if {self.vreg} == 0: goto {self.label.name}"

class VirtualRegister:
    def __init__(self):
        self._name = newUniqueName()

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return self.name

uniqueNameCounter = 0
def newUniqueName():
    global uniqueNameCounter
    uniqueNameCounter += 1
    return f"#{uniqueNameCounter}"