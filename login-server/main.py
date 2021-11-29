from websocket import create_connection
from flask import Flask, request, Response
import json
import uuid

# websocket client: https://github.com/Pithikos/websocket-client
GameServerPath = "ws://127.0.0.1:5001"
GameServerSecret = "secret"

app = Flask(__name__)


@app.route("/hello")
def hello():
    return 'HELLO WORLD!!!'


@app.route("/login", methods=['OPTIONS'])
def login_preflight():
    resp = Response("Hello from flask")
    resp.headers['Access-Control-Allow-Method'] = "POST"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type"
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route("/login", methods=['POST'])
def login():
    payload = json.loads(request.data)
    print(payload['id'], " has login...")

    token = str(uuid.uuid4())

    ws = create_connection(GameServerPath)
    
    setlogin = {
        "type": "login",
        "subtype": "set",
        "direction": "login-server2game-server",
        "server-key": GameServerSecret,
        "incoming-user-id": payload['id'],
        "incoming-user-token": token,
    }
    ws.send(json.dumps(setlogin))
    result =  ws.recv()
    if result != "close":
        print("Potential Game Server Error...")
    ws.close()
    
    response = {
        "id": payload['id'],
        "token": token
    }

    resp = Response(json.dumps(response))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


if __name__ == '__main__':
    app.run()