from qaviton_handlers.utils.log import log
from qaviton_handlers.utils.handle_failed_attempt import handle_failed_attempt


def retry(tries=3, delay=0, backoff=1, jitter=0, max_delay=None, exceptions=Exception, logger=log):
    """try a context of actions until attempts run out
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
        from qaviton_handlers.try_context import retry
        with retry() as trying:
            while trying:
                with trying:
                    print("Attempt #%d of %d" % (trying.attempt, trying.attempts))
                    raise
    """
    return TryManager(**locals()).trying


class TryManager:
    """ Context manager that counts attempts to run statements without
        exceptions being raised.
        - returns True when there should be more attempts
    """
    def __init__(self, tries, delay, backoff, jitter, max_delay, exceptions, logger):
        self.attempts = tries
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
    """ Context manager that only raises exceptions if its parent TryManager has given up. """
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
        if exc_type is None: self.manager.stop = True
        else: self.delay = handle_failed_attempt(
            exc_val,
            self.attempt,
            self.attempts,
            self.delay,
            self.backoff,
            self.jitter,
            self.max_delay,
            self.log)
        # Suppress exception if the manager is still trying.
        return bool(self.manager)

    def __bool__(self):
        return not self.manager.stop and self.manager.attempt < self.manager.attempts

    @property
    def attempt(self):
        return self.manager.attempt

    @property
    def attempts(self):
        return self.manager.attempts
