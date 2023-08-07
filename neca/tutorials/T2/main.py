import neca
from neca.events import event

@event("init")
def init(context, data):
    print("Hello, world!")

# starts the server and prevents the program from exiting
neca.start()