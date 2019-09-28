from sys import stderr


class dum_log:
    @staticmethod
    def warning(*args, **kwargs):
        stderr.write('\n'+' '.join(args))
