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