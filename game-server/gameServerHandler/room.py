import gameServerHandler.settings as settings
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
    # {"name": "room no.1", "id": "<uuidv4>", "owner-id": "jbc5740", "players": [{"id": "jbc5740", "ready": False}]}
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
    # {"name": "room no.1", "id": "<uuidv4>", "owner-id": "jbc5740", "players": [{"id": "jbc5740", "ready": False}]}
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
    # {"name": "room no.1", "id": "<uuidv4>", "owner-id": "jbc5740", "players": [{"id": "jbc5740", "ready": False}]}
    for room in settings.room_list:
        if room['id'] == json_obj['room-id']:
            for player in room['players']:
                if player['id'] == json_obj['user-id']: # Assume must find
                    player['ready'] = True # not sure if this works in python (if it push all the way into settings.room_list)
                    break

            allready = True
            for player in room['players']:
                if player['ready'] == False:
                    allready = False
            
            if allready == True:
                trigger_game_start_in_room(json_obj['room-id'], server)
    return

def trigger_game_start_in_room(room_id, server):
    payload = {
        "type": "game",
        "subtype": "map",
        "direction": "game-server2client",
        "map": "<not defined yet"
    }
    message = json.dumps(payload)
    for room in settings.room_list:
        if room['id'] == room_id:
            for player in room['players']:
                # search player in login list
                for user in settings.login_list:
                    if user['id'] == player['id']:
                        server.send_message(user['connection'], message)
            return



def player_unready(json_obj, client, server):
    for room in settings.room_list:
        if room['id'] == json_obj['room-id']:
            for player in room['players']:
                if player['id'] == json_obj['user-id']: # Assume must find
                    player['ready'] = False # not sure if this works in python (if it push all the way into settings.room_list)
                    return