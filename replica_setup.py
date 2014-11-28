import socket
from handlers  import handle_put, handle_get, handle_stats, handle_delete , update_stats , handle_commit, handle_abort
HOST = 'localhost'
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'STATS': handle_stats,
    'DEL': handle_delete,
    'COM' : handle_commit,
    'ABORT' : handle_abort,
    'KEYS': handle_keys
    }



def parse_message(data):
    """Return a tuple containing the command, the key, and (optionally) the
    value cast to the appropriate type."""
    print (data.strip().split(';') )
    seq, command, key, value = data.strip().split(';')
    return seq, command.upper(), key, value

def porcess_request(data):
    seq, command, key, value = parse_message(data)
    if command == 'STATS':
        response = handle_stats()
    elif command == 'GET':
        response = COMMAND_HANDLERS[command](key)
    elif command == 'DEL':
        response = COMMAND_HANDLERS[command](seq, key)
    elif command == 'PUT':
        response = COMMAND_HANDLERS[command](seq,key, value)
    elif command in ('COM','ABORT'):
        response = COMMAND_HANDLERS[command](seq)
    elif command == 'KEYS':
        response = COMMAND_HANDLERS[command]()
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