from sympy import Symbol


class Polynomial:
    def __init__(self, raw):
        self.raw = raw.lower()

    def parse(self):
        s = self.raw.split(' ')

        try:
            n = int(s[0])
        except ValueError:
            n = None

        if n:
            x = Symbol(s[1])
        else:
            x = Symbol(s[0])

        if len(s) == 1:
            return x, x
        elif s[1] == 'squared':
            return x ** 2, x
        elif s[1] == 'cubed':
            return x ** 3, x
