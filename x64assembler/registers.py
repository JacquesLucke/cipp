from . bits import Bits

class RegisterSpace:
    def __init__(self, size):
        assert size >= 0
        self.size = size

class RegisterSpaceSlice:
    def __init__(self, start, end):
        assert 0 <= start <= end
        self.start = start
        self.end = end

    @property
    def size(self):
        return self.end - self.start + 1

class Register:
    def __init__(self, name, space, spaceSlice):
        assert spaceSlice.end < space.size
        self.name = name
        self.space = space
        self.spaceSlice = spaceSlice

    @property
    def size(self):
        return self.spaceSlice.size

    def __repr__(self):
        return f"<Register: {self.name}, {self.size} bits>"

class GeneralPurposeRegister(Register):
    def __init__(self, name, identifier, space, spaceSlice):
        super().__init__(name, space, spaceSlice)
        self.number = identifier % 8
        self.bits = Bits.fromInt(self.number, length = 3)
        self.group = 1 if identifier >= 8 else 0


slice64Bit = RegisterSpaceSlice(0, 63)
slice32Bit = RegisterSpaceSlice(0, 31)
slice16Bit = RegisterSpaceSlice(0, 15)

def buildGPRegisterType1(id, letter):
    space = RegisterSpace(64)
    return (
        GeneralPurposeRegister(f"r{letter}x", id, space, slice64Bit),
        GeneralPurposeRegister(f"e{letter}x", id, space, slice32Bit),
        GeneralPurposeRegister(f"{letter}x", id, space, slice16Bit)
    )

def buildGPRegisterType2(id, letters):
    space = RegisterSpace(64)
    return (
        GeneralPurposeRegister(f"r{letters}", id, space, slice64Bit),
        GeneralPurposeRegister(f"e{letters}", id, space, slice32Bit),
        GeneralPurposeRegister(letters, id, space, slice16Bit)
    )

def buildGPRegisterType3(id):
    space = RegisterSpace(64)
    return (
        GeneralPurposeRegister(f"r{id}", id, space, slice64Bit),
        GeneralPurposeRegister(f"r{id}d", id, space, slice32Bit),
        GeneralPurposeRegister(f"r{id}w", id, space, slice16Bit)
    )

beforeCreation = set(globals().keys())

rax, eax, ax = buildGPRegisterType1(0, "a")
rbx, ebx, bx = buildGPRegisterType1(3, "b")
rcx, ecx, cx = buildGPRegisterType1(1, "c")
rdx, edx, dx = buildGPRegisterType1(2, "d")

rsp, esp, sp = buildGPRegisterType2(4, "sp")
rbp, ebp, bp = buildGPRegisterType2(5, "bp")
rsi, esi, si = buildGPRegisterType2(6, "si")
rdi, edi, di = buildGPRegisterType2(7, "di")

r8,  r8d,  r8w = buildGPRegisterType3(8)
r9,  r9d,  r9w = buildGPRegisterType3(9)
r10, r10d, r10w = buildGPRegisterType3(10)
r11, r11d, r11w = buildGPRegisterType3(11)

r12, r12d, r12w = buildGPRegisterType3(12)
r13, r13d, r13w = buildGPRegisterType3(13)
r14, r14d, r14w = buildGPRegisterType3(14)
r15, r15d, r15w = buildGPRegisterType3(15)

afterCreation = set(globals().keys())

registerNames = afterCreation - beforeCreation
allRegisters = {name : globals()[name] for name in registerNames}
