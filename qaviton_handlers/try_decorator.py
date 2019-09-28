from qaviton_handlers.utils.log import dum_log
from functools import wraps
from logging import Logger
from qaviton_handlers.utils.handle_failed_attempt import handle_failed_attempt


def retry(tries=3, delay=0, backoff=1, jitter=0, max_delay=None, exceptions=Exception, logger: Logger = dum_log):
    """Retry function decorator.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
                    fixed if a number, random if a range tuple (min, max), functional if callable (function must receive **kwargs)
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max), functional if callable (function must receive **kwargs)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    usage:
        from qaviton_handlers.try_decorator import retry

        @retry()
        def foo():
            n = int('1'+input('select number:'))
            print(n)

        foo()
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            wait = delay
            attempt = 0
            while tries == -1 or attempt < tries:
                attempt += 1
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    if attempt == tries: raise e
                    wait = handle_failed_attempt(e, attempt, tries, wait, backoff, jitter, max_delay, logger)
        return wrapper
    return decorator
