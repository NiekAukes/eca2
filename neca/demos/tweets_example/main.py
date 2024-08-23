import neca
from neca.events import *
from neca.generators import generate_data

generate_data("weer.txt", time_scale=1000)

# your code here
@event("init")
def init(ctx, data):
    print("init")

@event("tweet")
def tweet(ctx, data):
    print("tweeted")
    emit("x", data)


# starts the server and prevents the program from exiting
neca.start()