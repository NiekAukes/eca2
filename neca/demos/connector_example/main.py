import neca
from neca.events import *
from neca.connectors import connect_datastream

rs = Ruleset()
dataContext = create_context(name='Data Context', ruleset=rs)

# when running this, you should replace the ip with the ip of your server
connect_datastream('192.168.1.166', 25565, dataContext.fire)

@rs.event("button1")
def button1(ctx, data):
    print("button1 pressed")

@rs.event("button2")
def button2(ctx, data):
    print("button2 pressed")

@rs.event("button3")
def button3(ctx, data):
    print("button3 pressed")

@rs.event("button4")
def button4(ctx, data):
    print("button4 pressed")

@rs.event("custom")
def custom(ctx, data):
    print("custom event fired")
    print(data)


# starts the server and prevents the program from exiting
neca.start()