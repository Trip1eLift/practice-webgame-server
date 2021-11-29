# To share globals accross file within this package

# Need to actually handle mutex lock later for scaling and concurrency.
def init():
    global login_list
    login_list = []
    # [{
    #   "id": json_obj['incoming-user-id'],
    #   "token": json_obj['incoming-user-token'],
    #   "time": "later",
    #   "connection": client_obj => {'id':client_id, 'handler':client_handler, 'address':(addr, port)}
    # }]

    global room_list
    room_list = []
    # [{
    #   "name": "room no.1", 
    #   "id": "<uuidv4>", 
    #   "owner-id": "jbc5740", 
    #   "players": [{"id": "jbc5740", "ready": False}]
    # }]


def check_login(json_obj):
    global login_list #???? not sure about the syntax
    for user in login_list:
        if user['id'] == json_obj['user-id'] and user['token'] == json_obj['user-token']:
            # Implement time in user later
            return True

    return False