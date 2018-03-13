class Token:
    CONSUMED = 1
    CONSUMED_LAST = 2
    NOT_CONSUMED = 3

    @classmethod
    def startswith(cls, char):
        raise NotImplementedError()

    def __init__(self, firstChar):
        pass

    def checkNext(self, char):
        '''
        returns one of following constants:
            CONSUMED
            CONSUMED_LAST
            NOT_CONSUMED
        '''
        raise NotImplementedError()

    def isFinished(self):
        raise NotImplementedError()

    def __repr__(self):
        return f"<{type(self).__name__}>"

    

    