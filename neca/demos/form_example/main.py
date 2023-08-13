import neca
from neca.events import *
from neca.settings import app
from flask import request, jsonify

@app.route("/form", methods=["POST"])
def form():
    print(request.json)
    emit("form", request.json)
    return "", 200


# starts the server and prevents the program from exiting
neca.start()