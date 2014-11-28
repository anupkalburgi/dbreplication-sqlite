from datastore import DataStore

STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'DEL': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0},
    'COM': {'success': 0, 'error': 0},
    'ABORT': {'success': 0, 'error': 0},
    'KEYS': {'success': 0, 'error': 0}
}

DATA = {}
POROCESSING = []

def update_stats(command, success):
    """Update the STATS dict with info about if executing
    *command* was a *success*."""
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1


def handle_put(seq,key, value):
    """Return a tuple containing True and the message
    to send back to the client."""

    if key not in POROCESSING:
        POROCESSING.append(key)
        ds = DataStore(key,value)
        if ds.put(seq):
            POROCESSING.remove(key)
            return (True, 'Key [{}] set to [{}]'.format(key, value))
    return (False, 'Error:1')


def handle_get(key):
    """Return a tuple containing True if the key exists and the message
    to send back to the client."""
    if key not in POROCESSING:
        ds = DataStore()
        data = ds.get(key)
        if data:
            return(True, (data[0],data[1]))
    return(False, 'ERROR: Key [{}] not found'.format(key))
        


# def handle_putlist(key, value):
#     """Return a tuple containing True if the command succeeded and the message
#     to send back to the client."""
#     return handle_put(key, value)


# def handle_getlist(key):
#     """Return a tuple containing True if the key contained a list and
#     the message to send back to the client."""
#     return_value = exists, value = handle_get(key)
#     if not exists:
#         return return_value
#     elif not isinstance(value, list):
#         return (
#             False,
#             'ERROR: Key [{}] contains non-list value ([{}])'.format(key, value)
#             )
#     else:
#         return return_value


# def handle_increment(key):
#     """Return a tuple containing True if the key's value could be incremented
#     and the message to send back to the client."""
#     return_value = exists, value = handle_get(key)
#     if not exists:
#         return return_value
#     elif not isinstance(value, int):
#         return (
#             False,
#             'ERROR: Key [{}] contains non-int value ([{}])'.format(key, value)
#             )
#     else:
#         DATA[key] = value + 1
        # return (True, 'Key [{}] incremented'.format(key))


# def handle_append(key, value):
#     """Return a tuple containing True if the key's value could be appended to
#     and the message to send back to the client."""
#     return_value = exists, list_value = handle_get(key)
#     if not exists:
#         return return_value
#     elif not isinstance(list_value, list):
#         return (
#             False,
#             'ERROR: Key [{}] contains non-list value ([{}])'.format(key, value)
#             )
#     else:
#         DATA[key].append(value)
#         return (True, 'Key [{}] had value [{}] appended'.format(key, value))


def handle_delete(seq,key):
    """Return a tuple containing True if the key could be deleted and
    the message to send back to the client.

    Monty -- use datastore.get and then before doing doing datastore.delete
    """
    ds = DataStore()
    if ds.get(key):
        POROCESSING.append(key)
        if ds.delete(seq,key):   
            POROCESSING.remove(key)
            return (True,'Done')
        else:
            POROCESSING.remove(key)
    return (False,'ERROR: Key [{}] not found and could not be deleted'.format(key))

def handle_commit(seq):
    ds = DataStore()
    if ds.commit(seq):
        return (True,'Commit')
    else:
        return (False,'Error:')

def handle_abort(seq):
    ds = DataStore()
    if ds.roll_back(seq):
        return (True,'SEQ Aborted')
    return (False,"Error")


def handle_stats():
    """Return a tuple containing True and the contents of the STATS dict."""
    return (True, str(STATS))

def handle_keys():
    ds = DataStore()
    keys = ds.mykeys()
    keys = [x[0] for x in keys]
    keys_n =  ‘-‘.join(list1)
    return (True,keys_n)
