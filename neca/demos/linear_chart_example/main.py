import sys
sys.path.append("C:\\Users\\Nieka\\Documents\\Projects\\eca2")

import neca
from neca.events import *

@event("init")
def init(context, data):
    print("init")

@event("connect")
def connect(context, data):
    emit('chart', {
        'action': 'set',
        'series': 'series1',
        'value': [[1, 2], [2, 3], [3, 4]]
    })
    fire_global('add', None, delay=2)

@event("add")
def add45(context, data):
    emit('chart', {
        'action': 'add',
        'series': 'series1',
        'value': [4, 5]
    })

# starts the server and prevents the program from exiting
neca.start()