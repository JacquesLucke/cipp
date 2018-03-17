from lexer import Token, CharState

def createSingleCharToken(allowedChars):
    class SingleCharToken(Token):
        @classmethod
        def startswith(cls, char):
            return char in allowedChars

        def __init__(self, firstChar):
            self.value = firstChar

        def checkNext(self, char):
            return CharState.NOT_CONSUMED

        def __repr__(self):
            return f"<Token: {self.value}>"

    return SingleCharToken

singleChars = "(){}[],=+-*/@;<>"
SingleCharToken = createSingleCharToken(singleChars)

class WhitespaceToken(Token):
    whitespaceChars = tuple(" \t\n\r")

    @classmethod
    def startswith(cls, char):
        return char in cls.whitespaceChars

    def checkNext(self, char):
        if char in self.whitespaceChars:
            return CharState.CONSUMED
        else:
            return CharState.NOT_CONSUMED

asciiLowerCase = "abcdefghijklmnopqrstuvwxyz"
asciiUpperCase = asciiLowerCase.upper()
asciiLetters = asciiLowerCase + asciiUpperCase
digits = "0123456789"

class IdentifierToken(Token):
    @classmethod
    def startswith(cls, char):
        return char in asciiLetters or char == "_"

    def __init__(self, firstChar):
        self.value = firstChar

    def checkNext(self, char):
        if char in asciiLetters or char in digits or char == "_":
            self.value += char
            return CharState.CONSUMED
        else:
            return CharState.NOT_CONSUMED

    def __repr__(self):
        return f"<{type(self).__name__}: {self.value}>"

class IntegerToken(Token):
    @classmethod
    def startswith(cls, char):
        return char in digits

    def __init__(self, firstChar):
        self.content = firstChar

    def checkNext(self, char):
        if char in digits:
            self.content += char
            return CharState.CONSUMED
        elif char in asciiLetters:
            return CharState.INVALID
        else:
            return CharState.NOT_CONSUMED

    @property
    def value(self):
        return int(self.content)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.value}>"

class CommentToken(Token):
    @classmethod
    def startswith(cls, char):
        return char == "#"

    def __init__(self, firstChar):
        self.commentFinished = False
        self.value = ""

    def checkNext(self, char):
        if self.commentFinished:
            return CharState.NOT_CONSUMED
        if char == "\n":
            self.commentFinished = True
        else:
            self.value += char
        return CharState.CONSUMED

    def __repr__(self):
        return f"<{type(self).__name__}: {self.value}>"