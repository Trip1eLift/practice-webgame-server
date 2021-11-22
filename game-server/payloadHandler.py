from gameServerHandler.login import login_handler
from gameServerHandler.room import room_handler
from gameServerHandler.game import game_handler
import gameServerHandler.settings

gameServerHandler.settings.init()

def onmessage(json_obj, client, server):
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

test = {}
test['type'] = 'login'
onmessage(test)

#input('Press ENTER to exit')



