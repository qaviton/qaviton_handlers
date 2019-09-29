# Qaviton Handlers  
![logo](https://www.qaviton.com/wp-content/uploads/logo-svg.svg)  
[![version](https://img.shields.io/pypi/v/qaviton_handlers.svg)](https://pypi.python.org/pypi)
[![open issues](https://img.shields.io/github/issues/qaviton/qaviton_handlers)](https://github/issues-raw/qaviton/qaviton_handlers)
[![downloads](https://img.shields.io/pypi/dm/qaviton_handlers.svg)](https://pypi.python.org/pypi)
![code size](https://img.shields.io/github/languages/code-size/qaviton/qaviton_handlers)
-------------------------  

error handling utilities  
  
## Installation  
```sh  
pip install --upgrade qaviton_handlers  
```  
  
### Requirements
- Python 3.6+  
  
## Features  
* retry decorator ✓  
* retry with context ✓  
* try functions ✓  
* catch errors ✓  
* simple Exception wrapper ✓  

## Usage  
  
```python
def retry(tries=3, delay=0, backoff=1, jitter=0, max_delay=None, exceptions=Exception, logger: Logger = log):
    """Retry function decorator \ try a context of actions until attempts run out
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
                    fixed if a number, random if a range tuple (min, max), functional if callable (function must receive **kwargs)
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max), functional if callable (function must receive **kwargs)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled."""
```  
#### retry decorator
```python
from qaviton_handlers.try_decorator import retry

@retry()
def foo():
    n = int('1'+input('select number:'))
    print(n)

foo()
```
  
#### retry with context
```python
from qaviton_handlers.try_context import retry

with retry() as trying:
    while trying:
        with trying:
            print("Attempt #%d of %d" % (trying.attempt, trying.attempts))
            raise
```
  
#### using different try wrapper functions
```python
from qaviton_handlers.try_functions import try_to, try_or_none, multi_try, multi_try_no_break

def foo(a=0):
    print(float(a+input("select number:")))

# simply try
try_to(foo, 1)
try_to(foo, 2)
try_to(foo, 3)
```
```python
# get the error
error = try_to(foo, 4)
if error: print(error)

# if error occurred
if try_to(foo, 5):
    try_to(foo, 5)
```
```python
# try with key arguments
r = try_to(lambda a,b,c:a*b*c, 1,kwargs={'b':2,'c':3})
print(r)
```
```python
# try to get a number
number = try_or_none(lambda a:float(a+input("select number:")), 6)
if number: print(number)
```
```python
# try many functions, return a list of results, or an error
# if an error occurred, the multi try stops
multi_try(
  lambda: foo(10), 
  lambda: foo(11), 
)

# specify errors to ignore
response = multi_try(
  lambda: foo(13),
  lambda: foo(14),
  exceptions=Exception,
)

# handle the error
response = multi_try(
  lambda: foo(13),
  lambda: foo(14),
)
if isinstance(response, Exception):
    ...
```
```python
# try many functions, return a list of results, some may be errors
# if an error occurred, the multi try continues
multi_try_no_break(
    lambda: foo(8),
    lambda: foo(9),
    lambda: foo(0),
)
```
  
#### ignore errors now so you can handle them later
```python
from qaviton_handlers.catch import Catch
from qaviton_handlers.utils.error import Error

catch = Catch(store=True)

# catch an error
try:
    1 + '1'
except Exception as e:
    catch(e)

# a cleaner syntax
with catch:
    1 + '1'
    2 + '2'

# ignore the error
with Catch():
    5 * 'e'
    
print(f"caught {catch.count} errors")
print(f"caught first {catch.first}")
print(f"caught last {catch.last}")

# make your own Catch
class MyCatch(Catch):
    def handler(self, e):
        self.stack.add(Error(e))
        if self.log:
            self.log.warning(f"I caught {e}")
        return self
```  
  