class NoSetException(Exception):
    def __init__(self, *args):
        self.name = 'NoSetException'

        if args:
            self.message = ' '.join(args)
        else:
            self.message = None

    def __str__(self):
        if not self.message:
            return self.name

        return self.name + ':' + self.message

class NoPlayersException(Exception):
    def __init__(self, *args):
        self.name = 'NoPlayersException'

        if args:
            self.message = ' '.join(args)
        else:
            self.message = None

    def __str__(self):
        if not self.message:
            return self.name

        return self.name + ':' + self.message