from cord_handler import put, get , cdel

COMMAND_HANDLERS = {
    'PUT': put,
    'GET': get,
    'DEL': cdel
    }

STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'DEL': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0}
}


def update_stats(command, success):
    """Update the STATS dict with info about if executing
    *command* was a *success*."""
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1


def parse_message(data):
    """Return a tuple containing the command, the key, and (optionally) the
    value cast to the appropriate type."""
    print (data.strip().split(';') )
    command, key, value = data.strip().split(';')
    return command.upper(), key, value

def porcess_request(data):
    command, key, value = parse_message(data)
    if command == 'STATS':
        response = handle_stats()
    elif command == 'GET':
        response = COMMAND_HANDLERS[command](key)
    elif command == 'DEL':
        response = COMMAND_HANDLERS[command](key)
    elif command == 'PUT':
        response = COMMAND_HANDLERS[command](key, value)
    else:
        response = (False, 'Unknown command type [{}]'.format(command))
    update_stats(command, response[0])
    return '{};{}'.format(response[0], response[1])