from qaviton_handlers.utils.error import Error


class Catch:
    """in cases where you find yourself needing to ignore errors now so you can handle them later
    usage:
        from qaviton_handlers.catch import Catch
        catch = Catch()

        try:
            1+'1'
        except Exception as e:
            catch(e)

        with catch():
            1+'1'
            2+'2'

        print(f"caught {catch.count} errors")
        print(f"caught first {catch.first}")
        print(f"caught last {catch.last}")
    """
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

    @property
    def first(self):
        return min(self.stack)

    @property
    def last(self):
        return max(self.stack)

    def handler(self, e):
        error = Error(e)
        self.stack.add(error)
        return self

    def clean(self):
        self.__init__()

    def raise_e(self, error=None):
        if error:
            self(error)
            raise error
        for error in self.stack:
            raise error.e

    def raise_first(self):
        raise self.first.e

    def raise_last(self):
        raise self.last.e