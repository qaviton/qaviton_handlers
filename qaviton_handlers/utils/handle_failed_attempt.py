from time import sleep
from random import randint
from qaviton_handlers.utils.error import Error


def handle_failed_attempt(e, attempt, tries, delay, backoff, jitter, max_delay, log):
    if log: log.warning(f"{Error(e)}\nAttempt {attempt} of {tries}\nDelay: {delay}")

    if isinstance(jitter, tuple): sleep(delay + randint(*jitter))
    if callable(jitter): sleep(jitter(**locals()))
    else: sleep(delay + jitter)

    if isinstance(backoff, tuple): delay = delay * randint(*backoff)
    if callable(jitter): delay = backoff(**locals())
    else: delay = delay * backoff

    if max_delay:
        if max_delay < delay:
            delay = max_delay
    return delay
