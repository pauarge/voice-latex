from sympy import Symbol
import re

expr = r'([0-9]+)?(?:\s)?(times|divided)?(?:\s)?([a-zA-Z]+)(?:\s)?(squared|cubed)?'


class Polynomial:
    def __init__(self, raw):
        self.raw = raw.lower()

    def generate_without_factor(self, variable, power):
        if power == 'squared':
            return variable ** 2
        elif power == 'cubed':
            return variable ** 3
        else:
            return variable

    def parse(self):
        p = re.compile(expr)
        groups = p.search(self.raw).groups()

        factor = int(groups[0]) if groups[0] else None
        operation = groups[1]
        variable = Symbol(groups[2])
        power = groups[3]

        if factor:
            return factor * self.generate_without_factor(variable, power), variable
        else:
            return self.generate_without_factor(variable, power), variable
