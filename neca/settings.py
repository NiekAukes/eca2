from flask import Flask, render_template, url_for
from flask_socketio import SocketIO as Sock
import threading
import neca.events as events
import pathlib


"""
This module contains the global settings for the application.
and is used for defining the global variables.
"""
def init():
    global app
    global socket
    global eventThread

    app = Flask("__main__")
    socket = Sock(app, async_mode='threading')
    eventThread = threading.Thread(target=events.Manager.eventLoop)