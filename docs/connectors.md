# Connector
The connector are a way to let outside services generate events for your dashboard. They
allow websites, services, and other things to send events to your dashboard. 

## Connecting to an outside service
to connect to outside services, you first need to import the `connect_datastream` function from the `neca.connectors` module.

```python
from neca.connectors import connect_datastream
```

this function has the following arguments:
- `host`: the hostname to connect to (example.com)
- `port`: the port to connect to (probably 25565)
- `fire`: the fire function to call when an event is received (usually `fire_global`)

upon calling this function, it will connect to the datastream and forward any events to the fire function.

## Running your own connector middleware
we also provide a way to run your own connector middleware. this is useful if you want to test your dashboard without connecting to an official server. To do this, download the [connector middleware](https://github.com/NiekAukes/eca2/blob/main/connector%20middleware/connector.py) and run it with python. it will start a server on port 25565. you can then connect to this server with the `connect_datastream` function.

this server also comes with a web interface. you can access it by going to `http://localhost:5001` in your browser. this interface allows you to send events to the server. you can use this to test your dashboard.