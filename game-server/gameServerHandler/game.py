

def game_handler(json_obj):
    if json_obj['type'] != 'game':
        return None