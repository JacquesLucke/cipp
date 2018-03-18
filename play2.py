import sys
from cipp.parser import parse
from cipp.ast_to_ir import transformProgramToIR
from cipp.ir_to_x64 import compileToX64
from exec_utils import createFunctionFromHex
from ctypes import CFUNCTYPE, c_int

# with open("example_code") as f:
#     code = f.read()

code = '''
    def int @myfunc(int x, int y) {
        while (x <= y) {
            x = x + 1;
        }
        x = x + 100;
        return x;
    }
'''

ast = parse(code)
module = transformProgramToIR(ast)
# print(module.functions[0].block)

block = compileToX64(module.functions[0])
# print()
print(block.toIntelSyntax())
# sys.exit()

hexCode = block.toMachineCode().toHex()
f = createFunctionFromHex(CFUNCTYPE(c_int, c_int, c_int), hexCode)

print(f(0, 10))

