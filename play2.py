from cipp_parser import astFromString
from ast_to_ir.ast_to_ir import transformProgramToIR
from ir_to_x64.ir_to_x64 import compileToX64
from exec_utils import createFunctionFromHex
from ctypes import CFUNCTYPE, c_int

# with open("example_code") as f:
#     code = f.read()

code = '''
    def int @myfunc(int x, int y) {
        x = x + 10 - 1;
        return x+(3+y) - 10;
    }
'''

ast = astFromString(code)
module = transformProgramToIR(ast)
block = compileToX64(module.functions[0])
hexCode = block.toMachineCode().toHex()

f = createFunctionFromHex(CFUNCTYPE(c_int, c_int, c_int), hexCode)
print(f(10, 22))

