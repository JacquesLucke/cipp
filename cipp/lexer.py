class Lexer:
    def __init__(self, allowedTokens, ignoredTokens = []):
        self.allTokenTypes = allowedTokens
        self.ignoredTokenTypes = ignoredTokens

    def tokenize(self, charIterator):
        if isinstance(charIterator, str):
            charIterator = iter(charIterator)
        return list(TokenIterator(self, charIterator))

    def findMatchingTokenType(self, char):
        for tokenType in self.allTokenTypes:
            if tokenType.startswith(char):
                return tokenType
        raise Exception(f"token not recognized based on first char: '{char}'")

    def isTokenIgnored(self, token):
        return type(token) in self.ignoredTokenTypes


class Token:
    @classmethod
    def startswith(cls, char):
        raise NotImplementedError()

    def __init__(self, firstChar):
        pass

    def checkNext(self, char):
        '''return CharState'''
        raise NotImplementedError()

    def isFinished(self):
        return True

    def __repr__(self):
        return f"<{type(self).__name__}>"
    

class CharState:
    CONSUMED = 1
    NOT_CONSUMED = 2
    INVALID = 3


class TokenIterator:
    def __init__(self, lexer, charIterator):
        self.lexer = lexer
        self.chars = charIterator
        self.nextChar = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.getNextNotIgnoredToken()

    def getNextNotIgnoredToken(self):
        while True:
            token = self.getNextToken()
            if not self.lexer.isTokenIgnored(token):
                return token

    def getNextToken(self):
        if self.nextChar is None:
            # might raise StopIteration
            self.nextChar = next(self.chars)

        tokenType = self.lexer.findMatchingTokenType(self.nextChar)
        token = tokenType(self.nextChar)

        for char in self.chars:
            state = token.checkNext(char)
            if state == CharState.CONSUMED:
                continue
            elif state == CharState.NOT_CONSUMED:
                self.nextChar = char
                return token
            elif state == CharState.INVALID:
                raise Exception(f"invalid char: '{char}' must not directly follow {token}")
            else:
                raise Exception("unknown token state")

        if token.isFinished():
            self.nextChar = None
            return token
        else:
            raise Exception("could not finish token")