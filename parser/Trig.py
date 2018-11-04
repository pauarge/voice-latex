class Trig:
    def __init__(self, op, var):
        self.op = op
        self.var = var

    def parse(self):
        return '\{}({})'.format(self.op, self.var)
