# Extending your web server with Flask
## Flask
the neca web server is based on flask, a python web framework. this means that you can use flask to extend your web server with new features, such as new endpoints or pages (if that's desired).

new endpoints can be used to transfer data from your brows

to use the flask framework, you need to import it and import the app object from `neca.settings`.
```python
from flask import Flask
from neca.settings import app, socket
```

for more information about flask, visit the [flask documentation](https://flask.palletsprojects.com/en/2.0.x/).

### Adding a new endpoint
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

### Adding a new page
to add a new page, you need to use the `render_template` function from flask. this function takes the name of the template as an argument.
```python
from flask import render_template

@app.route('/hello')
def hello():
    return render_template('hello.html') # returns the contents of the 'hello.html' template
```

templates are stored in the `templates` folder. see the [templates](https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates) section of the flask documentation for more information.