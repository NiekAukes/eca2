import sys
sys.path.append("C:\\Users\\Nieka\\Documents\\Projects\\eca2")

import neca
from neca.events import *

@event("init")
def init(context, data):
    fire_global("init10", None, delay=10)

@event("init10")
def init10(context, data):
    emit('chart', {
        'action': 'set',
        'series': 'series1',
        'value': [[1, 2], [2, 3], [3, 4]]
    })

    emit('chart', {
        'action': 'add',
        'series': 'series1',
        'value': [4, 5]
    })

# starts the server and prevents the program from exiting
neca.start()