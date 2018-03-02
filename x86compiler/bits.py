class Bits:
    def __init__(self, bits):
        self.assertStringRepresentsBits(bits)
        self._bits = bits

    @staticmethod
    def assertStringRepresentsBits(string):
        assert isinstance(string, str)
        assert all(c == "0" or c == "1" for c in string)

    @classmethod
    def fromPosInt(cls, number, length = None):
        assert number >= 0

        binary = bin(number)[2:]
        if length is None:
            return cls(binary)

        binary = binary.zfill(length)
        if len(binary) > length:
            raise Exception("number requires more bits than specified by length")
        return cls(binary)

    @classmethod
    def fromHex(cls, hexNumber):
        if len(hexNumber) == 0:
            return Bits("")
        number = int(hexNumber, base = 16)
        length = len(hexNumber) * 4
        return cls.fromPosInt(number, length)

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
        fullHex = ""
        for i in range(0, len(self), 4):
            fullHex += hexCodes[self._bits[i:i+4]]
        return fullHex

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


# eg: "1100" -> "C"
hexCodes = {bin(i)[2:].zfill(4) : hex(i)[-1:].upper() for i in range(16)}
