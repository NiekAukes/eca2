from flask import Flask, render_template, url_for
from flask_socketio import SocketIO as Sock

import eca.events as events
import threading
import logging
import json


app = Flask(__name__)
socket = Sock(app, async_mode='threading')

# put logging level to error
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

# route to the index page
@app.route('/')
def index():
    return render_template("index.html")


def emit(event, data, id=None):
    """
    Emits a new event to the outside world (which is usually the browser).

    name: the name of the emitted event
    data: a piece of data that can be converted to JSON through json.dumps
    id: optional identifier to be emitted. None indicates no identifier is emitted.

    """
    if id is not None:
        data.update({"id": id})
    socket.emit(event, data)

@socket.on('connect')
def connect():
    print("connected")
    
@socket.on('disconnect')
def disconnect():
    print("disconnected")

eventThread = None

def start(debug=True):
    # start the event loop on a separate thread
    global eventThread
    eventThread = threading.Thread(target=events.Manager.eventLoop)
    eventThread.start()
    
    
    #app.run(debug=debug, use_reloader=False)
    socket.run(app, debug=debug, use_reloader=False)


if __name__ == '__main__':
    start()