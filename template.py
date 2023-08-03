from neca import *
from neca.events import *
from neca.log import logger
import logging
import random

# see what the engine is doing
# set to logging.WARNING to suppress info messages, etc
logger.setLevel(logging.DEBUG)  



## You might have to update the root path to point to the correct path
## (by default, it points to <rules>_static)
# root_content_path = 'template_static'


# binds the 'setup' function as the action for the 'init' event
# the action will be called with the context and the event
@event('init')
def setup(ctx, e):
    ctx["count"] = 0
    ctx.fire('sample', {'previous': 0.0})


# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

@event('sample')
def generate_sample(ctx, e):
    ctx["count"] += 1
    if ctx["count"] % 50 == 0:
        emit('debug', {'text': 'Log message #'+str(ctx["count"])+'!'})

    # base sample on previous one
    sample = clip(-100, e['previous'] + random.uniform(+5.0, -5.0), 100)

    # emit to outside world
    emit('sample',{
        'action': 'add',
        'value': sample
    })

    # chain event
    ctx.fire('sample', {'previous': sample}, delay=0.05)
    

start()