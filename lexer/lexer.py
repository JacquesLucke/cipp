from . token import Token

class TokenCollection:
    def __init__(self, tokenTypes):
        self.tokenTypes = tokenTypes

    def tokenize(self, string):
        pass

    def findMatchingTokenType(self, char):
        for tokenType in self.tokenTypes:
            if tokenType.startswith(char):
                return tokenType
        raise Exception("no token found")

class Lexer:
    def __init__(self, tokenCollection, charIterator):
        self.tokens = tokenCollection
        self.chars = charIterator
        self.i = 0
        self.nextChar = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.nextChar is None:
            # might raise StopIteration
            self.nextChar = next(self.chars)

        tokenType = self.tokens.findMatchingTokenType(self.nextChar)
        token = tokenType(self.nextChar)

        for char in self.chars:
            result = token.checkNext(char)
            if result == Token.CONSUMED:
                continue
            elif result == Token.CONSUMED_LAST:
                self.nextChar = None
                return token
            elif result == Token.NOT_CONSUMED:
                self.nextChar = char
                return token
            else:
                raise Exception("unknown token state")

        if token.isFinished():
            self.nextChar = None
            return token
        else:
            raise Exception("could not finish token")

    