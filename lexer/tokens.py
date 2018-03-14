from . token import Token, CharState

class SingleCharToken(Token):
    char = NotImplemented

    @classmethod
    def startswith(cls, char):
        return cls.char == char

    def checkNext(self, char):
        return CharState.NOT_CONSUMED

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if len(cls.char) != 1:
            raise Exception("expected class to have a single char")


class RoundBracketOpenToken(SingleCharToken):
    char = "("

class RoundBracketCloseToken(SingleCharToken):
    char = ")"

class CommaToken(SingleCharToken):
    char = ","

class EqualToken(SingleCharToken):
    char = "="

class CurlyRoundBracketOpenToken(SingleCharToken):
    char = "{"

class CurlyRoundBracketCloseToken(SingleCharToken):
    char = "}"

class PlusToken(SingleCharToken):
    char = "+"

class MinusToken(SingleCharToken):
    char = "-"

class StarToken(SingleCharToken):
    char = "*"

class SlashToken(SingleCharToken):
    char = "/"

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
        self.content = firstChar

    def checkNext(self, char):
        if char in asciiLetters or char in digits or char == "_":
            self.content += char
            return CharState.CONSUMED
        else:
            return CharState.NOT_CONSUMED

    def __repr__(self):
        return f"<{type(self).__name__}: {self.content}>"

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
    def number(self):
        return int(self.content)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.number}>"



def createTokenTypeFromLetter(letter):
    class ReprMeta(type):
        def __repr__(cls):
            return letter

    class LetterToken(Token, metaclass = ReprMeta):
        @classmethod
        def startswith(cls, char):
            return letter == char

        def checkNext(self, char):
            return CharState.NOT_CONSUMED

        def __repr__(self):
            return letter

    return LetterToken