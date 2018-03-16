from clipp.parser import astFromString

with open("example_code") as f:
    code = f.read()

ast = astFromString(code)
print(ast.functions)