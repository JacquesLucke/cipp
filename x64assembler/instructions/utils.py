from .. bits import Bits

def getImmSize(n):
    if n == 0:
        return 0
    elif -2**7 <= n <= 2**7 - 1:
        return 1
    elif -2**15 <= n <= 2**15 - 1:
        return 2
    elif -2**31 <= n <= 2**31 - 1:
        return 4
    elif -2**63 <= n <= 2**64 - 1:
        return 8
    else:
        raise NotImplementedError("unsupported immediate value size")


def getRegGroupPrefix_64(reg1, reg2):
    return prefixesFor64BitRegs[(reg1.group, reg2.group)]

def getRegGroupPrefix_32(reg1, reg2):
    return prefixesFor32BitRegs[(reg1.group, reg2.group)]

prefixesFor64BitRegs = {
    (0, 0) : Bits.fromHex("48"),
    (1, 0) : Bits.fromHex("49"),
    (0, 1) : Bits.fromHex("4c"),
    (1, 1) : Bits.fromHex("4d")
}

prefixesFor32BitRegs = {
    (0, 0) : Bits.fromHex(""),
    (1, 0) : Bits.fromHex("41"),
    (0, 1) : Bits.fromHex("44"),
    (1, 1) : Bits.fromHex("45")
}