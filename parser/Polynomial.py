class Polynomial:
    def __init__(self, raw):
        self.raw = raw.lower()

    def parse(self):
        splitted = self.raw.split(' ')
        if len(splitted) == 1:
            return splitted[0]
        elif splitted[1] == 'squared':
            return '{}**2'.format(splitted[0])
        elif splitted[1] == 'cubed':
            return '{}**3'.format(splitted[0])
