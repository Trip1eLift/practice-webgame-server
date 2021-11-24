import json
import settings

def login_handler(json_obj, client, server):
    if json_obj['type'] != 'login':
        return
    if json_obj['subtype'] == 'set':
        set_login(json_obj, client, server)
    elif json_obj['subtype'] == 'client':
        client_login_attempt(json_obj, client, server)

def set_login(json_obj, client, server):
    # check if user is already logged in
    logged_in = False
    for user in settings.login_list:
        if user['id'] == json_obj['incoming-user-id']:
            logged_in = True
            break
    if logged_in == True:
        server.send_message(client, "close")

    if json_obj['server-key'] == "secret":
        user = {
            "id": json_obj['incoming-user-id'],
            "token": json_obj['incoming-user-token'],
            "time": "later"
        }
        settings.login_list.append(user)
    server.send_message(client, "close")
    return

def client_login_attempt(json_obj, client, server):
    logged_in = False
    for user in settings.login_list:
        if user['id'] == json_obj['user-id']:
            logged_in = True
            break
    payload = {
        "type": "login",
        "subtype": "client",
        "direction": "game-server2client",
    }
    if logged_in == True:
        payload['result'] = "allow"
    else:
        payload['result'] = "deny"
        
    message = json.dumps(payload)
    server.send_message(client, message)
    return