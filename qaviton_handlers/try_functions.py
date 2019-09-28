import time
import traceback
from sys import stderr
from functools import wraps
from qaviton_handlers.error import Error


def try_to(f, *args, exceptions=Exception, **kwargs):
    try: return f(*args, **kwargs)
    except exceptions as e: return e


def try_or_none(f, *args, exceptions=Exception, **kwargs):
    try: return f(*args, **kwargs)
    except exceptions: return


def multi_try(*f, exceptions=Exception): return try_to(lambda: [F() for F in f], exceptions=exceptions)
def multi_try_no_break(*f, exceptions=Exception): return [try_to(F, exceptions=exceptions) for F in f]


class dum_log:
    @staticmethod
    def warning(*args, **kwargs):
        stderr.write('\n'+' '.join(args))


def retry(retries=3, delay=0, backoff=1, jitter=0, max_delay=None, exceptions=Exception, logger=dum_log):
    """Retry function decorator.
    you can also put in delay and backoff to wait between retries
    and define to which exception you want to retry.
    :param retries: number of times to try (not retry) before giving up
    :param delay: initial delay between retries in seconds
    :param backoff: backoff multiplier e.g. value of 2 will double the delay each retry
    :param exceptions: the exception to check. may be a tuple of exceptions to check
    :type retries: int
    :type delay: int
    :type backoff: int
    :type exceptions: Exception or tuple
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            wait = delay
            for i in range(retries):
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    error = Error(e)
                    logger.warning(f"{error}\nRetries left {retries-i}")
                    time.sleep(wait)
                    wait = wait*backoff+jitter
                    if max_delay:
                        if max_delay < wait:
                            wait = max_delay
            return f(*args, **kwargs)
        return wrapper
    return decorator


def Retry(retries=3, delay=0, backoff=1, jitter=0, max_delay=None, exceptions=Exception, logger=dum_log):
    return TryManager(**locals()).trying


class TryManager:
    """ Context manager that counts attempts to run statements without
        exceptions being raised.
        - returns True when there should be more attempts
    """
    def __init__(self, retries, delay, backoff, jitter, max_delay, exceptions, logger):
        self.attempts = retries
        self.attempt = -1
        self.stop = False
        self.trying = Trying(self, delay, backoff, jitter, max_delay, exceptions, logger)

    def __call__(self, *args, **kwargs):
        return self.trying

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __bool__(self):
        return not self.stop and self.attempt < self.attempts


class Trying:
    """ Context manager that only raises exceptions if its parent
        RetryManager has given up."""
    def __init__(self, manager: TryManager, delay, backoff, jitter, max_delay, exceptions, logger):
        self.manager = manager
        self.delay = delay
        self.backoff = backoff
        self.jitter = jitter
        self.max_delay = max_delay
        self.exceptions = exceptions
        self.log = logger

    def __enter__(self):
        if self.attempts > -1:
            self.manager.attempt += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.manager.stop = True
        else:
            error = Error(exc_val)
            self.log.warning(f"{error}\nAttempt {self.attempt} of {self.attempts}")
            time.sleep(self.delay)
            self.delay = self.delay*self.backoff+self.jitter
            if self.max_delay:
                if self.max_delay < self.delay:
                    self.delay = self.max_delay

        # Suppress exception if the retry manager is still alive.
        return bool(self.manager)

    def __bool__(self):
        return not self.manager.stop and self.manager.attempt < self.manager.attempts

    @property
    def attempt(self):
        return self.manager.attempt

    @property
    def attempts(self):
        return self.manager.attempts

with Retry() as trying:
    while trying:
        with trying:
            # print("Attempt #%d of %d" % (trying.attempt, trying.attempts))
            raise
