from cipp_parser import astFromString
from ast_to_ir.ast_to_ir import transformProgramToIR

with open("example_code") as f:
    code = f.read()

code = '''
    def void @myfunc(int x, int y) {
        x = 5;
        return x*(3+4);
    }
'''

ast = astFromString(code)
module = transformProgramToIR(ast)