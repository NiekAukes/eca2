from flask import Flask, render_template, request, redirect, url_for, flash
import socket
import json
from threading import Thread, Lock
from time import sleep

app = Flask(__name__)
csockets = [] # list of connected sockets
socket_lock = Lock() # lock for the list of sockets

# =============================================================================================
#                                        Web app routes
# =============================================================================================
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Simulator</title>
        </head>
        <body>
            <div class="buttongrid">
                <div class="button" id="button1">Button 1</div>
                <div class="button" id="button2">Button 2</div>
                <div class="button" id="button3">Button 3</div>
                <div class="button" id="button4">Button 4</div>
            </div>
            <div class="custom">
                <input type="text" id="custom" placeholder="Custom event">
                <textarea id="customdata" placeholder="Custom data">{\n    "myKey":"myValue"\n}</textarea>
                <button id="custombutton">Send</button>
            </div>
            <script>
                var buttons = document.getElementsByClassName("button");
                for (var i = 0; i < buttons.length; i++) {
                    buttons[i].addEventListener("click", function() {
                        var key = this.id;
                        var data = {
                            "button": key
                        }
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "/" + key, true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.send(JSON.stringify(data));
                    });
                }

                var custombutton = document.getElementById("custombutton");
                custombutton.addEventListener("click", function() {
                    var key = document.getElementById("custom").value;
                    var data = document.getElementById("customdata").value;
                    try {
                        var json = JSON.parse(data);
                    } catch (e) {
                        // if the data is not json, send it as a string
                        var json = data;
                    }

                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/" + key, true);
                    xhr.setRequestHeader('Content-Type', json instanceof Object ? 'application/json' : 'text/plain');
                    xhr.send(json instanceof Object ? JSON.stringify(json) : json);
                });
            </script>
            <style>
                /* Basic Button Styling */
                .button {
                    display: flex;
                    justify-content: center;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    background-color: #007bff;
                    color: #fff;
                    cursor: pointer;
                    content-align: center;
                }

                .button:hover {
                    background-color: #006fe6;
                }

                .button:active {
                    background-color: #0056b3;
                }


                .buttongrid {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr 1fr;
                    grid-gap: 10px;
                    margin: 20px min(200px, 10%);
                }

                .custom {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-bottom: 20px;
                }

                .custom input {
                    margin-bottom: 10px;
                    min-width: min(300px, 80%);
                }

                .custom textarea {
                    margin-bottom: 10px;
                    min-width: min(400px, 80%);
                    min-height: 100px;
                }


            </style>
        </body>
    </html>
    """

@app.route("/<key>", methods=["POST"])
def event(key):
    # send event to all connected clients
    # with the accompanied data

    tosend = {
        "key": key,
        "data": request.json
    }

    # jsonize the data
    tosend = json.dumps(tosend) + "\n"

    # send to all connected clients
    socket_lock.acquire()
    for csocket in csockets:
        try:
            csocket.send(tosend.encode("utf-8"))
        except:
            # if the client is not connected anymore, remove it from the list
            csockets.remove(csocket)
    socket_lock.release()

    return "OK", 200

def listener(list, lock):
    while True:
        clientsocket, address = s.accept()
        lock.acquire()
        list.append(clientsocket)
        lock.release()
        print(f"Connection from {address} has been established!")

# =============================================================================================
#                                   Connecting with clients
# =============================================================================================
# the idea of this app is to forward all events to connected clients
# the clients will be connected via network sockets
# a website will send events to this app
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 25565))

    # print the port number
    print(f"Listening on port {s.getsockname()}")

    s.listen()
    


    # start a thread that listens for new connections
    t = Thread(target=listener, args=(csockets, socket_lock))
    t.start()



# =============================================================================================
#                                       Running the app
# =============================================================================================
    app.run(debug=False, port=5001)
