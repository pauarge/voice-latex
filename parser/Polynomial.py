from sympy import Symbol


class Polynomial:
    def __init__(self, raw):
        self.raw = raw.lower()

    def parse(self):
        splitted = self.raw.split(' ')
        x = Symbol(splitted[0])
        if len(splitted) == 1:
            return x, x
        elif splitted[1] == 'squared':
            return x ** 2, x
        elif splitted[1] == 'cubed':
            return x ** 3, x
