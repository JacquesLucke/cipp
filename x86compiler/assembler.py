class AssemblyInstruction:
    def toMachineCode():
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

class BitString:
    def __init__(self):
        self.bits = b""

    @classmethod
    def fromZeroOneString(cls, bits):
        bitString = cls()
        bitString.bits = bytes(int(c) for c in bits)
        return bitString

    @classmethod
    def fromNumber(cls, number, bits):
        s = bin(number)[2:].zfill(bits)
        if len(s) > bits:
            raise Exception("number is too larger for bit amount")
        return cls.fromZeroOneString(s)

    @classmethod
    def fromHex(cls, hexNumber):
        return cls.fromNumber(int(hexNumber, base = 16), bits = len(hexNumber) * 4)

    @classmethod
    def join(cls, *args):
        bitString = cls()
        for arg in args:
            bitString.bits += arg.bits
        return bitString

    def toHex(self):
        return hex(self.toNumber())

    def toNumber(self):
        return int(self.toZeroOneString(), base = 2)

    def toZeroOneString(self):
        return "".join(str(b) for b in self.bits)

    def __add__(self, other):
        bitString = BitString()
        bitString.bits = self.bits + other.bits
        return bitString

    def __len__(self):
        return len(self.bits)

    def __repr__(self):
        return self.toZeroOneString()


class Register:
    def __init__(self, name, bits):
        self.name = name
        self.bits = bits

    @property
    def number(self):
        return self.bits.toNumber()

class TwoOpInstruction(AssemblyInstruction):
    opcode = NotImplemented
    name = NotImplemented

    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

    def toMachineCode(self):
        # indicates that the R/M field is a register
        mod = BitString.fromZeroOneString("11")

        return BitString.join(self.opcode, mod, self.source.bits, self.destination.bits)

    def __repr__(self):
        return f"{self.name} {self.destination.name}, {self.source.name}"

class AddInstruction(TwoOpInstruction):
    opcode = BitString.fromHex("01")
    name = "add"

class MoveInstruction(TwoOpInstruction):
    opcode = BitString.fromHex("89")
    name = "mov"

class RetInstruction(AssemblyInstruction):
    def toMachineCode(self):
        return BitString.fromHex("C3")

    def __repr__(self):
        return "ret"

class PushInstruction(AssemblyInstruction):
    def __init__(self, reg):
        self.reg = reg

    def toMachineCode(self):
        return BitString.fromNumber(int("50", base = 16) + self.reg.number, bits = 8)

    def __repr__(self):
        return f"push {self.reg}"

class Registers:
    eax = Register("EAX", BitString.fromZeroOneString("000"))
    ebx = Register("EBX", BitString.fromZeroOneString("011"))
    ecx = Register("ECX", BitString.fromZeroOneString("001"))
    edx = Register("EDX", BitString.fromZeroOneString("010"))

add = AddInstruction(eax, ebx)
print(add.toMachineCode().toHex())

mov = MoveInstruction(eax, ebx)
print(mov.toMachineCode().toHex())

push = PushInstruction(ebx)
print(push.toMachineCode().toHex())
