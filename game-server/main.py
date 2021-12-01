from websocket_server import WebsocketServer
import json
from payloadHandler import *

# Websocket server docs: https://github.com/Pithikos/python-websocket-server
HOST = "0.0.0.0"
PORT = 5001

def WS_Starts():
    server = WebsocketServer(host=HOST, port=PORT)

    def new_connection(client, server):
        print("New client has connected to the server")
        print(f"ID: {client['id']}, Address: {client['address']}")
        return

    def on_recieve(client, server, message):
        payload = json.loads(message)
        message = f"ID: {client['id']} has sent message: " + json.dumps(payload)
        print(message)

        onmessage(payload, client, server)
        return

    def on_close(client, server):
        # needs to handle disconnection cleanup
        print(f"ID: {client['id']}, Address: {client['address']}", " has left.")
        return

    server.set_fn_new_client(new_connection)
    server.set_fn_message_received(on_recieve)
    server.set_fn_client_left(on_close)
    print("Listening on: ws://" + HOST + ":" + str(PORT))
    server.run_forever()

    return 'TERMINATE'

if __name__ == "__main__":
    WS_Starts()