from . grammar import Grammar, NonTerminalSymbol
from . token_stream import TokenStream, EOFToken

def checkIfStringMatchesGrammar(string, lexer, grammar):
    tokens = list(lexer.tokenize(string))
    checkIfTokenStreamMatchesGrammar(TokenStream(tokens), grammar)

def checkIfTokenStreamMatchesGrammar(tokens, grammar):
    table = grammar.createParsingTable()
    stack = [EOFToken, grammar.start]

    while len(stack) > 0:
        stackTop = stack.pop()
        token = tokens.peekNext()
        tokenType = type(token)

        if isinstance(stackTop, NonTerminalSymbol):
            entry = (stackTop, tokenType)
            if entry in table:
                stack.extend(table[entry][::-1])
            else:
                raise Exception(f"no parser table entry for {entry}")
        elif stackTop == tokenType:
            tokens.take(1)
        else:
            raise Exception(f"unexpected token: {token}")

    if len(stack) > 0:
        raise Exception("missing tokens at the end")