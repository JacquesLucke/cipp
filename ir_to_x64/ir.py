class ModuleIR:
    def __init__(self, functions):
        self.functions = functions

class FunctionIR:
    def __init__(self, name):
        self.name = name
        self.arguments = []
        self.instructions = InstructionListIR()

    def addArgument(self):
        reg = VirtualRegister()
        self.arguments.append(reg)
        return reg
    
    def getUsedVRegisters(self):
        registers = set()
        registers.update(self.arguments)
        registers.update(self.instructions.iterUsedVRegisters())
        return registers

    def __repr__(self):
        return f"{self.name} ({', '.join(map(str, self.arguments))})\n{self.instructions}"

class InstructionListIR:
    def __init__(self):
        self.instructions = []
        self.labels = {}

    def add(self, instruction):
        self.instructions.append(instruction)

    def newLabel(self, prefix):
        i = 0
        while True:
            i += 1
            label = f"{prefix}_{i}"
            if label not in self.labels:
                break
        self.labels[label] = None
        return label

    def insertLabelAfterCurrentInstruction(self, label):
        self.labels[label] = len(self.instructions)

    def iterUsedVRegisters(self):
        for instr in self.instructions:
            yield from instr.getVRegisters()

    def __iter__(self):
        return iter(self.instructions)

    def __repr__(self):
        return "\n".join(self._iterReprLines())

    def _iterReprLines(self):
        labelByIndex = self.getLabelsByIndex()
        for i, instr in enumerate(self.instructions):
            if i in labelByIndex:
                yield f"{labelByIndex[i]}:"
            yield str(instr)

    def getLabelsByIndex(self):
        return {i : label for label, i in self.labels.items()}
    

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
        return f"goto {self.label}"

class GotoIfZeroIR(InstructionIR):
    def __init__(self, vreg, label):
        self.vreg = vreg
        self.label = label

    def getVRegisters(self):
        return [self.vreg]

    def __repr__(self):
        return f"if {self.vreg} == 0: goto {self.label}"

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