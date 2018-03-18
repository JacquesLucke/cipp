import sys
from cipp_parser import astFromString
from ast_to_ir.ast_to_ir import transformProgramToIR
from ir_to_x64.ir_to_x64 import compileToX64
from exec_utils import createFunctionFromHex
from ctypes import CFUNCTYPE, c_int

# with open("example_code") as f:
#     code = f.read()

code = '''
    def int @myfunc(int x, int y) {
        while (x <= y) {
            x = x + 1;
        }
        return x;
    }
'''

ast = astFromString(code)
module = transformProgramToIR(ast)
print(module.functions[0].block)

block = compileToX64(module.functions[0])
# print()
# print(block.toIntelSyntax())
# sys.exit()

hexCode = block.toMachineCode().toHex()
f = createFunctionFromHex(CFUNCTYPE(c_int, c_int, c_int), hexCode)

print(f(0, 10))

