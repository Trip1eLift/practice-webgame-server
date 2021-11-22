

def room_handler(json_obj):
    if json_obj['type'] != 'room':
        return None