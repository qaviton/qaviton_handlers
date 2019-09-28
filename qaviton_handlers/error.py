from traceback import format_tb


class Error:
    def __init__(self, e: Exception):
        self.trace: str = ''.join(format_tb(e.__traceback__))
        self.type: str = type(e)
        self.value: str = str(e)

    def __str__(self):
        return f'Error Traceback:\n{self.trace}{self.type.__name__}: {self.value}'

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
