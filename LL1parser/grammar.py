from . token_stream import EOFToken
from lexer.token import isTokenClass

# http://www.jambe.co.nz/UNI/FirstAndFollowSets.html
# http://www.cs.virginia.edu/~cs415/reading/FirstFollowLL.pdf

class Grammar:
    def __init__(self, start, rules):
        self.start = start
        self.rules = rules

    def first(self, elements):
        '''
        Compute first tokens that can be matched by the element-list.
        Resulting set can also contain None.
        '''
        if not isinstance(elements, (list, tuple)):
            elements = [elements]

        if len(elements) == 0:
            return {None}

        if isTokenClass(elements[0]):
            return {elements[0]}

        firstSet = set()

        for production in self.rules[elements[0]]:
            if len(production) == 0:
                firstSet.update(self.first(elements[1:]))
            else:
                if isTokenClass(production[0]):
                    firstSet.add(production[0])
                else:
                    f = self.first(production[0])
                    if None in f:
                        firstSet.update(f - {None})
                        firstSet.update(self.first(production[1:] + elements[1:]))
                    else:
                        firstSet.update(f)
        
        return firstSet

    def follow(self, symbol):
        '''
        Compute tokens that are allowed to come after the given symbol.
        The resulting set can also contain EOFToken which means that the 
        input stream is allowed to end after the symbol.
        '''
        return self._follow(symbol, set())

    def _follow(self, symbol, seenRules):
        followSet = set()

        if self.start == symbol:
            followSet.add(EOFToken)

        for src, production in self.iterProductionsWithElement(symbol):
            index = production.index(symbol)
            f = self.first(production[index+1:])
            followSet.update(f - {None})

            ruleIdentifier = (src, tuple(production))
            if None in f and ruleIdentifier not in seenRules:
                seenRules.add(ruleIdentifier)
                followSet.update(self._follow(src, seenRules))
      
        return followSet

    def iterProductionsWithElement(self, element):
        yield from filter(lambda x: element in x[1], self.iterProductions())
        
    def iterProductions(self):
        for src, productions in self.rules.items():
            for production in productions:
                yield src, production

    def getTerminals(self):
        terminals = set()
        for _, production in self.iterProductions():
            terminals.update(filter(lambda x: isTokenClass(x), production))
        return terminals

    def createParsingTable(self):
        table = {}

        for symbol, production in self.iterProductions():
            f = self.first(production)
            for token in f:
                if token is not None:
                    table[(symbol, token)] = production
            
            if None in f:
                for token in self.follow(symbol):
                    table[(symbol, token)] = production

        return table

class NonTerminalSymbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(self) == type(other):
            return self.name == other.name
        return False
    
    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name