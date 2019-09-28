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
* catch errors and stack them ✓  
* simple try functions ✓  
* simple retry decorator ✓  
## Usage  
  
#### creating a flask app  
```python
# app.py
from flask import Flask
from qaviton_proxy import proxy

app = Flask(__name__)

@app.route("/prox", methods=['GET'])
def client_session():
    return proxy('https://proxied.com')

app.run(port=3000)
```
  
#### run the app
```sh
python app.py
```  
  
#### send request to app
```python
import requests
response = requests.get('localhost:3000/prox')  # send request to app
print(response.json())  # got response from 'localhost:3000/prox' which proxied 'https://proxied.com'  
```  
