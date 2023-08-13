import neca
from neca.events import *

@event("init")
def init(context, data):
    fire_global("init5", None, delay=5)

@event("init5")
def init5(context, data):
    emit("linechart", {
        "action": "set",
        "value": ["Sunday", 10]
    })

    emit("linechart", {
        "action": "add",
        "value": ["Monday", 20]
    })


# starts the server and prevents the program from exiting
neca.start()