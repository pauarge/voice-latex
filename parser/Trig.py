class Trig:
    def __init__(self, op, var, power):
        self.op = op
        self.var = var
        if power == 'square':
            self.power = 2
        elif power == 'cube':
            self.power = 3
        else:
            self.power = 1

    def parse(self):
        if self.power > 1:
            return '\{}^{}({})'.format(self.op, self.power, self.var)
        else:
            return '\{}({})'.format(self.op, self.var)
