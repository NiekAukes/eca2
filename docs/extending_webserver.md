the neca web server is based on flask, a python web framework. this means that you can use flask to extend your web server with new features, such as new endpoints or pages (if that's desired).

new endpoints can be used to transfer data from your brows

to use the flask framework, you need to import it and import the app object from `neca.settings`.
```python
from flask import Flask
from neca.settings import app, socket
```

for more information about flask, visit the [flask documentation](https://flask.palletsprojects.com/en/2.0.x/).

## Adding a new endpoint
to add a new endpoint, you need to use the `route` decorator from flask. this decorator takes the path of the endpoint as an argument.
```python
@app.route('/hello')
def hello():
    return 'hello world', 200 # returns 'hello world' with a status code of 200 (OK)

@app.route('/hello/<name>')
def hello_name(name):
    return f'hello {name}', 200 # returns 'hello <name>'
```

see the [routing](https://flask.palletsprojects.com/en/2.0.x/quickstart/#routing) section of the flask documentation for more information.

### forwarding requests to the event system
you can forward a request, from a form for example, to the event system with the following code:
```python
from flask import Flask, request
from neca.settings import app, socket
from neca.events import fire_global

@app.route('/hello', methods=['POST'])
def route():
    data = request.json # get the data from the request
    fire_global('my_event', data) # send the data to the event system
    return 'hello world', 200 # return a response
```

### initiating requests from javascript
you can initiate a request from javascript with `fetch()`. Here is an example:
```js
fetch('/hello', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'john doe',
        age: 42
    })
})
```

see the [fetch()](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) documentation for more information.

## Adding a new page
to add a new page, you need to use the `render_template` function from flask. this function takes the name of the template as an argument.
```python
from flask import render_template

@app.route('/hello')
def hello():
    return render_template('hello.html') # returns the contents of the 'hello.html' template
```

templates are stored in the `templates` folder. see the [templates](https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates) section of the flask documentation for more information.