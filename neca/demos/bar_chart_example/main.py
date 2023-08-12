import neca
from neca.events import *

@event("init")
def init(context, data):
    fire_global("init5", None, delay=10)

@event("init5")
def init5(context, data):
    emit("barchart", {
        "action": "set",
        "value": ["Red", 10]
    })

    emit("barchart", {
        "action": "add",
        "value": ["Yellow", 20]
    })


# starts the server and prevents the program from exiting
neca.start()