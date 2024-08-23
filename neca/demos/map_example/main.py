import neca
from neca.events import *
from neca.log import logger
import logging
import random

# see what the engine is doing
# set to logging.WARNING to suppress info messages, etc
logger.setLevel(logging.DEBUG)  

center = [52.221539, 6.893662]

@event('init')  # predefined event, called when the engine starts
def init(context, event):
    context.fire('random', [], delay=1)

@event('random')
def increment(context, data):
    x_offset = random.randint(-20, 20)
    y_offset = random.randint(-20, 20)
    x = center[0] + x_offset / 1000
    y = center[1] + y_offset / 1000
    data.append((x, y))
    emit("map", {
        "action": "draw",
        "type": "marker",
        "name": "mork",
        "coordinates": [x, y],
    })
    emit("map", {
        "action": "draw",
        "type": "circle",
        "name": "cork",
        "options": {
            "fillOpacity": 0.5,
            "radius": 300,
        },	
        "coordinates": center,
    })
    emit("map", {
        "action": "draw",
        "type": "line",
        "name": "lork",
        "options": {
            "color": "red",
            "weight": 5,
        },
        "coordinates": data,
    })
    
    context.fire('random', data, delay=1)

# starts the server and prevents the program from exiting
neca.start() 