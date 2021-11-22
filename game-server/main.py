from websocket_server import WebsocketServer
import json
from payloadHandler import *

# Websocket server docs: https://github.com/Pithikos/python-websocket-server
HOST = "127.0.0.1"
PORT = 5001

clients = []

def WStest():
    server = WebsocketServer(host=HOST, port=PORT)

    def new_connection(client, server):
        print("New client has connected to the server")
        print(f"ID: {client['id']}, Address: {client['address']}")
        clients.append(client)
        message = "clients list:"
        for c in clients:
            message = message + f" {c['id']},"
        server.send_message_to_all(message)
        return

    def on_recieve(client, server, message):
        data = json.loads(message)
        message = f"ID: {client['id']} has sent message: " + json.dumps(data)
        print(message)
        for c in clients:
            server.send_message(c, message)
        return

    def on_close(client, server):
        print(f"ID: {client['id']}, Address: {client['address']}", " has left.")
        clients.remove(client)
        return

    server.set_fn_new_client(new_connection)
    server.set_fn_message_received(on_recieve)
    server.set_fn_client_left(on_close)
    server.run_forever()

    return 'TERMINATE'

if __name__ == "__main__":
    WStest()