from sympy import Symbol
import re

expr = r'([0-9]+)?(?:\s)?(times|divided)?(?:\s)?([a-zA-Z]+)(?:\s)?(squared|cubed)?(?:\s)?(plus|minus)?'


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
        groups = p.findall(self.raw)
        parsed_groups = []

        for group in groups:
            factor = int(group[0]) if group[0] else None
            operation = group[1]
            variable = Symbol(group[2])
            power = group[3]

            if factor and operation == 'times':
                parsed_groups.append(factor * self.generate_without_factor(variable, power))
            elif factor and operation == 'divided':
                parsed_groups.append(factor / self.generate_without_factor(variable, power))
            else:
                parsed_groups.append(self.generate_without_factor(variable, power))

        res = parsed_groups[0]
        for i in range(1, len(groups)):
            res = res + parsed_groups[i]

        return res, variable
