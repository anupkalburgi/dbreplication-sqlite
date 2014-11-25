STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'DELETE': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0},
}

DATA = {}

def update_stats(command, success):
    """Update the STATS dict with info about if executing
    *command* was a *success*."""
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1


def handle_put(key, value):
    """Return a tuple containing True and the message
    to send back to the client."""
    DATA[key] = value
    return (True, 'Key [{}] set to [{}]'.format(key, value))


def handle_get(key):
    """Return a tuple containing True if the key exists and the message
    to send back to the client."""
    if key not in DATA:
        return(False, 'ERROR: Key [{}] not found'.format(key))
    else:
        return(True, DATA[key])


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


def handle_delete(key):
    """Return a tuple containing True if the key could be deleted and
    the message to send back to the client.

    Monty -- use datastore.get and then before doing doing datastore.delete
    """
    if key not in DATA:
        return (
            False,
            'ERROR: Key [{}] not found and could not be deleted'.format(key)
            )
    else:
        del DATA[key]


def handle_stats():
    """Return a tuple containing True and the contents of the STATS dict."""
    return (True, str(STATS))
