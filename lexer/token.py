class CharState:
    CONSUMED = 1
    NOT_CONSUMED = 2
    INVALID = 3

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

def isTokenClass(element):
    try: return issubclass(element, Token)
    except: return False
    