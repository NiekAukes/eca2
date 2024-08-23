""" ECA server module
This is the main module for the ECA server. It contains the start function
and provides access to the flask app object
"""

from flask import render_template, request
from flask_socketio import SocketIO as Sock


import logging
import neca.settings as settings
from neca.events import fire_global, event
from typing import Callable, Any
import types
import uuid


settings.init()
from neca.settings import app, socket, eventThread


# put logging level to error
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

# route to the index page
@app.route('/')
def index():
    return render_template("index.html")

def route(path: str, *args, **kwargs):
    """
    binds a POST route to an event with json data
    """
    def decorator(func: Callable):
        generated_eventname = "$$_" + str(uuid.uuid4())
        def groute(*args, **kwargs):
            kwargs = dict(kwargs)
            data = request.get_json()
            args += (data,)
            fire_global(generated_eventname, *args, **kwargs)
            return "OK", 200
        
        # I hate that I need to do this...
        # flask does not like it when you try to route a function with the SAME NAME as another function
        # so I need to create a new function object every time.... with a random name
        # KURVA!
        app.route(path, methods=["POST"], *args, **kwargs)(types.FunctionType(groute.__code__, globals(), name=str(uuid.uuid4()), argdefs=groute.__defaults__, closure=groute.__closure__))
        event(generated_eventname)(func)
        return func
    return decorator

# define signatures for predefined events
@event("init")
def init_event():
    pass

@event("connect")
def connect_event():
    pass

@event("disconnect")
def disconnect_event():
    pass

# provide handlers for socket events
@socket.on('connect')
def connect():
    fire_global('connect')
    
@socket.on('disconnect')
def disconnect():
    fire_global('disconnect')


def start(debug=True, port=5000):
    # start the event loop on a separate thread
    #settings.init()
    eventThread.start()
    
    
    #app.run(debug=debug, use_reloader=False)
    socket.run(app, 
               debug=debug, 
               use_reloader=False, 
               allow_unsafe_werkzeug=True,
               log_output=True,
               port=port)



if __name__ == '__main__':
    start()

