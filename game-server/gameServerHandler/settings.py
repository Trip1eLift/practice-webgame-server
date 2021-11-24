# To share globals accross file within this package

# Need to actually handle mutex lock later for scaling and concurrency.
def init():
    global login_list
    login_list = []
    global room_list
    room_list = []


def check_login(json_obj):
    global login_list #???? not sure about the syntax
    for user in login_list:
        if user['id'] == json_obj['user-id'] and user['token'] == json_obj['user-token']:
            # Implement time in user later
            return True

    return False