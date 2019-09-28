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

# get the error
error = try_to(foo, 4)
if error: print(error)

# if error occurred
if try_to(foo, 5):
    try_to(foo, 5)

# try to get a number
number = try_or_none(lambda a:float(a+input("select number:")), 6)
if number: print(number)

# try many functions, return a list of results, or an error
# if an error occurred, the multi try stops
multi_try(
    foo,
    foo,
    foo,
    lambda: foo(7),
    lambda: foo(7),
    lambda: foo(7),
)

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
```  
  