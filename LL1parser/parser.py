from lexer.token import Token

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def take(self, n):
        tokens = self.getLookahead(n)
        self.position += n
        return tokens

    def takeOrFail(self, tokenType):
        if isinstance(self.peekNext(), tokenType):
            return self.take(1)[0]
        else:
            raise Exception(f"found unexpected token: {self.peekNext()}")

    def getLookahead(self, n):
        if len(self) < n:
            raise Exception(f"cannot look ahead {n} tokens, only {len(self)} available")
        return self.tokens[self.position:self.position+n]

    def peekNext(self):
        return self.getLookahead(1)[0]

    def __len__(self):
        return len(self.tokens) - self.position


# http://www.jambe.co.nz/UNI/FirstAndFollowSets.html
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
                firstSet.add(None)
            else:
                if isTokenClass(production[0]):
                    firstSet.add(production[0])
                else:
                    f = self.first(production[0])
                    if None in f:
                        firstSet.update(f - {None})
                        firstSet.update(self.first(elements[1:]))
                    else:
                        firstSet.update(f)
        
        return firstSet

    def follow(self, symbol):
        '''
        Compute tokens that are allowed to come after the given symbol.
        The resulting set can also contain "$" which means that the 
        input stream is allowed to end after the symbol.
        '''
        followSet = set()

        if self.start == symbol:
            followSet.add("$")

        for src, production in self.iterProductionsWithElement(symbol):
            index = production.index(symbol)
            f = self.first(production[index+1:])
            followSet.update(f - {None})
            if None in f and src != symbol:
                followSet.update(self.follow(src))
      
        return followSet

    def iterProductionsWithElement(self, element):
        yield from filter(lambda x: element in x[1], self.iterProductions())
        
    def iterProductions(self):
        for src, productions in self.rules.items():
            for production in productions:
                yield src, production 

def isTokenClass(element):
    try: return issubclass(element, Token)
    except: return False  

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
        return f"<Symbol: {self.name}>"

