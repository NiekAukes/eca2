"""
This module contains the global settings for the application framework.
and is used for defining the global variables.
you can import 
"""
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO as Sock
import threading
import neca.events as events

# global variables
app = None
socket = None
eventThread = None


def init():
    global app
    global socket
    global eventThread

    app = Flask("__main__")
    socket = Sock(app, async_mode='threading')
    eventThread = threading.Thread(target=events.Manager.eventLoop, daemon=True)