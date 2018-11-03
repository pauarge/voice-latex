from sympy import Symbol


class Polynomial:
    def __init__(self, raw):
        self.raw = raw.lower()

    def parse(self):
        s = self.raw.split(' ')

        try:
            n = int(s[0])
            x = Symbol(s[1])
            if len(s) == 2:
                return n * x, x
            elif s[2] == 'squared':
                return n * x ** 2, x
            elif s[2] == 'cubed':
                return n * x ** 3, x

        except ValueError:
            x = Symbol(s[0])
            if len(s) == 1:
                return x, x
            elif s[1] == 'squared':
                return x ** 2, x
            elif s[1] == 'cubed':
                return x ** 3, x
