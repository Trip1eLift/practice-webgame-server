from gameServerHandler.login import login_handler
from gameServerHandler.room import room_handler
from gameServerHandler.game import game_handler
import gameServerHandler.settings

gameServerHandler.settings.init()

def onmessage(json_obj, client, server):
    # direction checking is not neccessary...
    if json_obj['direction'] != 'client2game-server' and json_obj['direction'] != 'login-server2game-server':
        return False
    if json_obj['type'] == 'login':
        login_handler(json_obj, client, server)
    elif json_obj['type'] == 'room':
        room_handler(json_obj, client, server)
    elif json_obj['type'] == 'game':
        game_handler(json_obj, client, server)
    else:
        return False
    return True


def printHello():
    print('Hello')





