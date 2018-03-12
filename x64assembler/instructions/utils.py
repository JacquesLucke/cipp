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
