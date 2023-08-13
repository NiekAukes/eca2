import socket
from threading import Thread
from time import sleep
from typing import Callable, List, Tuple, Any
import json

def connect_datastream(host: str, port: int, fire: Callable):
    """
    connects to a datastream at host:port, then fires the appropriate
    events when data is received
    host: the hostname to connect to (example.com)
    port: the port to connect to (25565)
    fire: the function to invoke when data is received
    """
    Thread(target=_connect, args=(host, port, fire)).start()
    
def _connect(host: str, port: int, fire: Callable):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print(str(e))
        return
    data = b''
    try:
        while True:
            # wait for data, append to buffer
            data += sock.recv(1024)
            # if there is a newline in the buffer, split the buffer
            if b'\n' in data:
                data = data.split(b'\n')

                # fire the event for each line
                for i in range(len(data) - 1):
                    # decode the data and decode the json
                    decoded = data[i].decode('utf-8')
                    unjsoned = json.loads(decoded)

                    # if the json does not have a key or data, skip it
                    if 'key' not in unjsoned or 'data' not in unjsoned:
                        continue

                    # get the key and data from the json
                    key = unjsoned['key']
                    d = unjsoned['data']

                    # fire the event
                    fire(key, d)

                # reset the buffer to the last line
                data = data[-1]
    except Exception as e:
        print('connection closed unexpectedly')