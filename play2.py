import sys
from cipp.parser import parse
from cipp.ast_to_ir import transformProgramToIR
from cipp.ir_to_x64 import compileModule
from exec_utils import createFunctionFromHex
from ctypes import CFUNCTYPE, c_longlong

# with open("example_code") as f:
#     code = f.read()

code = '''
    def int @fib(int n) {
        if (n <= 2) return 1;
        else return @fib(n-1) + @fib(n-2);
    }

    def int @pow(int base, int exponent) {
        let int result = 1;
        while (exponent > 0) {
            result = @mul(base, result);
            exponent = exponent - 1;
        }
        return result;
    }

    def int @mul(int x, int y) {
        let int result = 0;
        while (x > 0) {
            result = result + y;
            x = x - 1;
        }
        return result;
    }
'''

ast = parse(code)
module = transformProgramToIR(ast)
# print(module.functions[0].block)

block = compileModule(module)
# print()
print(block.toIntelSyntax())
# sys.exit()

hexCode = block.toMachineCode().toHex()
# print(hexCode)
f = createFunctionFromHex(CFUNCTYPE(c_longlong, c_longlong), hexCode)

print()
print(f(20))

