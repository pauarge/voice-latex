from sympy import Symbol


class Polynomial:
    def __init__(self, coefs):
        self.coefs = coefs

    def parse(self):
        k = len(self.coefs) - 1
        x = Symbol('x')
        res = self.coefs[0] * x ** k
        for i in range(1, len(self.coefs)):
            k = k - 1
            res = res + self.coefs[i] * x ** k
        return res
