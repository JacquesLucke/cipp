from . add_imm_to_reg import AddImmToRegInstr
from . mov_imm_to_reg import MovImmToRegInstr
from . mov_reg_to_reg import MovRegToRegInstr
from . mov_mem_to_reg import MovMemToRegInstr
from . mov_reg_to_mem import MovRegToMemInstr
from . push_reg import PushRegInstr
from . push_imm import PushImmInstr
from . syscall import SyscallInstr
from . pop_reg import PopRegInstr
from . ret import RetInstr

from . jumps import (
    JmpInstr, JmpNotZeroInstr, JmpZeroInstr
)

from . simple_two_reg import (
    AddRegToRegInstr, SubRegFromRegInstr, CompareInstr
)