class Bits:
    def __init__(self, bits):
        self.assertStringRepresentsBits(bits)
        self._bits = bits

    @staticmethod
    def assertStringRepresentsBits(string):
        assert isinstance(string, str)
        assert all(c == "0" or c == "1" for c in string), string

    @classmethod
    def fromInt(cls, number, length = None):
        if length is None:
            if number >= 0: return cls(bin(number)[2:])
            else: raise Exception("length has to be given when using negative integers")
        binary = intToBits(number, length)
        return cls(binary)

    @classmethod
    def fromHex(cls, hexNumber):
        if len(hexNumber) == 0:
            return Bits("")
        number = int(hexNumber, base = 16)
        length = len(hexNumber) * 4
        return cls.fromInt(number, length)

    @classmethod
    def join(cls, *args):
        return cls("".join(b._bits for b in args))

    def reversedBytes(self):
        length = len(self)
        assert length % 8 == 0
        newBits = ""
        for i in range(length - 8, -1, -8):
            newBits += self._bits[i:i+8]
        return Bits(newBits)

    def toString(self):
        return self._bits

    def toHex(self):
        assert len(self) % 4 == 0
        return "".join(hexCodes[p] for p in iterSequenceParts(self._bits, 4))

    def toCArrayInitializer(self):
        array = ", ".join("0x" + p for p in iterSequenceParts(self.toHex(), 2))
        return "{" + array + "}"

    def __eq__(self, other):
        return self._bits == other

    def __add__(self, other):
        return Bits(self._bits + other._bits)

    def __len__(self):
        return len(self._bits)

    def __repr__(self):
        return f"<Bits: {self._bits}>"

    def __int__(self):
        return int(self._bits, base = 2)

def iterSequenceParts(sequence, partLength):
    assert len(sequence) % partLength == 0
    for i in range(0, len(sequence), partLength):
        yield sequence[i:i+partLength]

# eg: "1100" -> "C"
hexCodes = {bin(i)[2:].zfill(4) : hex(i)[-1:].upper() for i in range(16)}


def intToBits(number, length):
    if number < 0:
        result = complement(bin(abs(number) - 1)[2:]).rjust(length, "1")
    else:
        result = bin(number)[2:].rjust(length, "0")
    if len(result) > length:
        raise Exception("number requires more bits than specified by length")
    return result

def complement(bitString):
    return "".join(complementDict[c] for c in bitString)

complementDict = {"0" : "1", "1" : "0"}
