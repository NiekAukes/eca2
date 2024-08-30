import neca
from neca.events import *
from neca.log import logger
import logging
import random
import json

# see what the engine is doing
# set to logging.WARNING to suppress info messages, etc
logger.setLevel(logging.DEBUG)  

@event("init")
def init(ctx, e):
    fire_global("random", None)
    
@event("connect")
def connect(ctx, e):
    emit('apex', {
        "action": "updateSeries",
        "newSeries": [{
            "name": "Random",
            "data": [random.randint(0, 100) for i in range(10)]
        }]
    })
    
    
@event("random")
def random_event(ctx, e):
    emit('apex', {
        "action": "appendData",
        "newData": [{
            "data": [random.randint(0, 100)],
        }]
    })
    ctx.fire("random", None, delay=1)
# starts the server and prevents the program from exiting
neca.start() 