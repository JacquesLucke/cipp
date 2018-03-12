from .. bits import Bits
from . instruction import Instruction

class AddRegToRegInstr(Instruction):
    def __init__(self, dstReg, srcReg):
        assert dstReg.size == srcReg.size
        self.dstReg = dstReg
        self.srcReg = srcReg
        self.regSize = self.dstReg.size