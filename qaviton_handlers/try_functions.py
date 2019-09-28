def try_to(f, *args, exceptions=Exception, **kwargs):
    try: return f(*args, **kwargs)
    except exceptions as e: return e


def try_or_none(f, *args, exceptions=Exception, **kwargs):
    try: return f(*args, **kwargs)
    except exceptions: return


def multi_try(*f, exceptions=Exception):
    return try_to(lambda: [F() for F in f], exceptions=exceptions)


def multi_try_no_break(*f, exceptions=Exception):
    return [try_to(F, exceptions=exceptions) for F in f]
