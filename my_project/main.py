import neca
from neca.events import *
from neca.log import logger
import logging

# see what the engine is doing
# set to logging.WARNING to suppress info messages, etc
logger.setLevel(logging.DEBUG)  


@event('init')  # predefined event, called when the engine starts
@condition(lambda c, e: e is None)  # only fire when the event data is none
def init(context, event):
    print("init")
    
    # fire the event "init" with data "not None", will be caught by the condition
    fire_global("init", "not None")  
    
    # same as the line above in this case, but can be useful when you have multiple contexts and rules
    context.fire("init", "not None")  


# starts the server and prevents the program from exiting
neca.start()