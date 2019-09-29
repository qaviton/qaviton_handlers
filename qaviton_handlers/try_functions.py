from logging import Logger


def try_to(f, *args, exceptions=Exception, logger: Logger = None, kwargs: dict = None):
    try:
        return f(*args, **kwargs if kwargs else {})
    except exceptions as e:
        if logger:
            logger.exception(e)
        return e


def try_or_none(f, *args, exceptions=Exception, logger: Logger = None, kwargs: dict = None):
    try:
        return f(*args, **kwargs if kwargs else {})
    except exceptions as e:
        if logger:
            logger.exception(e)
        return


def multi_try(*f, exceptions=Exception, logger: Logger = None):
    return try_to(lambda: [F() for F in f], exceptions=exceptions, logger=logger)


def multi_try_no_break(*f, exceptions=Exception, logger: Logger = None):
    return [try_to(F, exceptions=exceptions, logger=logger) for F in f]
