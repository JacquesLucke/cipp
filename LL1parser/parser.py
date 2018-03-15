from . grammar import Grammar, NonTerminalSymbol
from . token_stream import TokenStream, EOFToken

def checkIfStringMatchesGrammar(string, lexer, grammar):
    tokens = list(lexer.tokenize(string))
    return checkIfTokenStreamMatchesGrammar(TokenStream(tokens), grammar)

def checkIfTokenStreamMatchesGrammar(tokens, grammar):
    table = grammar.createParsingTable()
    stack = [EOFToken, grammar.start]
    treeStack = []

    while len(stack) > 0:
        stackTop = stack.pop()
        token = tokens.peekNext()
        tokenType = type(token)

        if isinstance(stackTop, NonTerminalSymbol):
            entry = (stackTop, tokenType)
            if entry in table:
                production = table[entry]
                node = ParseTreeNode(stackTop, production)
                stack.append(node)
                stack.extend(reversed(production))
            else:
                raise Exception(f"no parser table entry for {entry}")
        elif isinstance(stackTop, ParseTreeNode):
            node = stackTop
            count = node.elementCount
            if count > 0:
                node.setChildren(treeStack[-count:])
                del treeStack[-count:]
            else:
                node.setChildren([])
            treeStack.append(node)
        elif stackTop == tokenType:
            treeStack.append(tokens.take(1))
        else:
            raise Exception(f"unexpected token: {token}")

    return treeStack[0]

class ParseTreeNode:
    def __init__(self, symbol, production):
        self.symbol = symbol
        self.production = production

    def setChildren(self, children):
        self.children = children

    @property
    def elementCount(self):
        return len(self.production)

    def __repr__(self):
        return f"<Node: {self.symbol}>"

    def toTreeString(self):
        return "\n".join(self.iterTreeStringLines())

    def iterTreeStringLines(self):
        yield f"{self.symbol}:"
        for child in self.children:
            if isinstance(child, ParseTreeNode):
                for line in child.iterTreeStringLines():
                    yield "   |" + line
            else:
                yield "   |" + str(child)