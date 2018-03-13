from . token import Token

class SingleCharToken(Token):
    char = NotImplemented

    @classmethod
    def startswith(cls, char):
        return cls.char == char

    def checkNext(self, char):
        return Token.NOT_CONSUMED

    def isFinished(self):
        return True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if len(cls.char) != 1:
            raise Exception("expected class to have a single char")


class BracketOpenToken(SingleCharToken):
    char = "("

class BracketCloseToken(SingleCharToken):
    char = ")"

class CommaToken(SingleCharToken):
    char = ","

class WhitespaceToken(Token):
    whitespaceChars = tuple(" \t\n\r")

    @classmethod
    def startswith(cls, char):
        return char in cls.whitespaceChars

    def checkNext(self, char):
        if char in self.whitespaceChars:
            return Token.CONSUMED
        else:
            return Token.NOT_CONSUMED

    def isFinished(self):
        return True

asciiLowerCase = "abcdefghijklmnopqrstuvwxyz"
asciiUpperCase = asciiLowerCase.upper()
asciiLetters = asciiLowerCase + asciiUpperCase
digits = "0123456789"

class NameToken(Token):

    @classmethod
    def startswith(cls, char):
        return char in asciiLetters

    def __init__(self, firstChar):
        self.content = firstChar

    def checkNext(self, char):
        if char in asciiLetters or char in digits:
            self.content += char
            return Token.CONSUMED
        else:
            return Token.NOT_CONSUMED

    def __repr__(self):
        return f"<{type(self).__name__}: {self.content}>"