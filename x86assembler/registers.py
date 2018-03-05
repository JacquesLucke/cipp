from . bits import Bits

class Register:
    def __init__(self, name, bits):
        self.name = name
        self.bits = bits

    @property
    def number(self):
        return int(self.bits)

eax = Register("eax", Bits("000"))
ebx = Register("ebx", Bits("011"))
ecx = Register("ecx", Bits("001"))
edx = Register("edx", Bits("010"))

esp = Register("esp", Bits("100"))
ebp = Register("ebp", Bits("101"))
