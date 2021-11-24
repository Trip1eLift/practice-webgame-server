import settings
import json
import uuid

def room_handler(json_obj, client, server):
    if json_obj['type'] != 'room':
        return
    if settings.check_login(json_obj) == False:
        return
    
    if json_obj['subtype'] == 'list':
        list_room(json_obj, client, server)

    # The following 5 cases need to trigger list room to all players
    if json_obj['subtype'] == 'create':
        create_room(json_obj, client, server)
    elif json_obj['subtype'] == 'close':
        close_room(json_obj, client, server)
    elif json_obj['subtype'] == 'join':
        join_room(json_obj, client, server)
    elif json_obj['subtype'] == 'leave':
        leave_room(json_obj, client, server)
    elif json_obj['subtype'] == 'ready':
        player_ready(json_obj, client, server)
    elif json_obj['subtype'] == 'unready':
        player_unready(json_obj, client, server)
    else:
        return # Not trigger global_list_room

    global_list_room(server)
    return

def list_room(json_obj, client, server):
    payload = {
        "type": "room",
        "subtype": "list",
        "direction": "game-server2client",
        "rooms": settings.room_list
    }
    message = json.dumps(payload)
    server.send_message(client, message)
    return

def global_list_room(server):
    payload = {
        "type": "room",
        "subtype": "list",
        "direction": "game-server2client",
        "rooms": settings.room_list
    }
    message = json.dumps(payload)
    server.send_message_to_all(message)
    return


def create_room(json_obj, client, server):
    # {"name": "room no.1", "id": "<uuidv4>", "owner-id": "jbc5740", "players": [{"id": "jbc5740", "ready": true}]}
    room = {
        "name": json_obj['roomname'],
        "id": uuid.uuid4(),
        "owner-id": json_obj['user-id'],
        "players": [ 
            {
                "id": json_obj['user-id'],
                "ready": False
            } 
        ]
    }
    # allow repeat roomname
    settings.room_list.append(room)

    # return a roomlist to confirm the room is created

def close_room(json_obj, client, server):
    # only owner can close its own room
    # room close is expected to be successful
    for room in settings.room_list:
        if room['owner-id'] == json_obj['user-id'] and room['id'] == json_obj['room-id']:
            settings.room_list.remove(room)
            return

    print("Room unmatch, unexpected error")
    return

def join_room(json_obj, client, server):
    # Assume a player can only join room if not in any room
    # Therefore, no checking for if player is in a room already
    #{"name": "room no.1", "id": "<uuidv4>", "owner-id": "jbc5740", "players": ["jbc5740"]}
    for room in settings.room_list:
        if room['id'] == json_obj['room-id']:
            player = {
                "id": json_obj['user-id'],
                "ready": False
            }
            room['players'].append(player) # not sure if this works in python (if it push all the way into settings.room_list)
            return

    print("Room unmatch, unexpected error")
    return
            
def leave_room(json_obj, client, server):
    # Assume a player can only leave room if the player is in the room
    # Disallow owner to leave the room
    for room in settings.room_list:
        if room['id'] == json_obj['room-id'] and room['owner-id'] != json_obj['user-id']:
            target_player = {}
            for player in room['players']:
                if player['id'] == json_obj['user-id']: # Assume must find
                    target_player = player
            room['players'].remove(target_player) # not sure if this works in python (if it push all the way into settings.room_list)
            return

    print("Room unmatch, unexpected error")
    return

def player_ready(json_obj, client, server):
    # if all players in room are ready
    #  0. mutex lock
    #  1. start the game (login list need to store client)
    #  2. remove the room
    return

def player_unready(json_obj, client, server):
    return