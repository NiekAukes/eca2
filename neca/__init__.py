""" ECA server module
This is the main module for the ECA server. It contains the start function
and provides access to the flask app object
"""

from flask import render_template
from flask_socketio import SocketIO as Sock


import logging
import neca.settings as settings



settings.init()
from neca.settings import app, socket, eventThread


# put logging level to error
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

# route to the index page
@app.route('/')
def index():
    return render_template("index.html")


@socket.on('connect')
def connect():
    print("connected")
    
@socket.on('disconnect')
def disconnect():
    print("disconnected")


def start(debug=True):
    # start the event loop on a separate thread
    #settings.init()
    eventThread.start()
    
    
    #app.run(debug=debug, use_reloader=False)
    socket.run(app, debug=debug, use_reloader=False)


if __name__ == '__main__':
    start()

