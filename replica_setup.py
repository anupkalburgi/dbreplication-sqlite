import socket
from handlers  import handle_put, handle_get, handle_stats, handle_delete , update_stats
HOST = 'localhost'
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'STATS': handle_stats,
    'DELETE': handle_delete
    }



def parse_message(data):
    """Return a tuple containing the command, the key, and (optionally) the
    value cast to the appropriate type."""
    command, key, value, value_type = data.strip().split(';')
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command, key, value

def porcess_request(data):
    command, key, value = parse_message(data)
    if command == 'STATS':
        response = handle_stats()
    elif command in ('GET','DELETE'):
        response = COMMAND_HANDLERS[command](key)
    elif command in ('PUT'):
        response = COMMAND_HANDLERS[command](key, value)
    else:
        response = (False, 'Unknown command type [{}]'.format(command))
    update_stats(command, response[0])
    return '{};{}'.format(response[0], response[1])

def main():
    """Main entry point for script."""
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)
    while 1:
        connection, address = SOCKET.accept()
        print 'New connection from [{}]'.format(address)
        data = connection.recv(4096).decode()
        command, key, value = parse_message(data)
        if command == 'STATS':
            response = handle_stats()
        elif command in ('GET','DELETE'):
            response = COMMAND_HANDLERS[command](key)
        elif command in ('PUT'):
            response = COMMAND_HANDLERS[command](key, value)
        else:
            response = (False, 'Unknown command type [{}]'.format(command))
        update_stats(command, response[0])
        connection.sendall('{};{}'.format(response[0], response[1]))
        connection.close()

if __name__ == '__main__':
    main()