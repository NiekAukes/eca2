import neca
from neca.events import *

@event("init")
def init(context, data):
    print("init")

@event("connect")
def connect(context, data):
    emit('piechart', {
        'action': 'set',
        'value': ['Blue', 5]
    })

    emit('piechart', {
        'action': 'add',
        'value': ['Green', 15]
    })

    fire_global('after5', None, delay=5)

@event("after5")
def after5(context, data):
    emit("piechart", {
        "action": "set",
        "value": ["Red", 10]
    })

    emit("piechart", {
        "action": "add",
        "value": ["Blue", 20]
    })


# starts the server and prevents the program from exiting
neca.start()