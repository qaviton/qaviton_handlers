from qaviton_handlers.error import Error


class Catch:
    def __init__(self):
        self.stack = set()

    def __call__(self, error):
        return self.handler(error)

    def __len__(self):
        return len(self.stack)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.handler(exc_val)
            return True

    @property
    def count(self):
        return len(self)

    def clean(self):
        self.__init__()

    def add(self, error):
        self.stack.add(error)

    def Raise(self, error):
        self.add(error)
        raise error

    def raise_first(self):
        raise min(self.stack)

    def raise_last(self):
        raise max(self.stack)

    def handler(self, e):
        error = Error(e)
        self.stack.add(error)
