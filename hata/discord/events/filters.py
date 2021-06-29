__all__ = ()

from ...backend.export import include

Client = include('Client')


def filter_clients(clients, flag_mask):
    """
    Filters the clients whether their intents allows the specific flag.
    
    First yields the first client from `clients` what allows the specified flag. If non, then yields `None`.
    If a `None` or not the expected client was yielded, then the generator should be closed.
    
    If the correct client was yielded, then the generator is used at a for loop yielding all the clients from `clients`
    which allow the specified flag including the firstly yielded one.
    
    This function is a generator.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        The clients to filter.
    flag_mask : `int`
        The intent flag's mask based on what the clients will be filtered.
    
    Yields
    -------
    client : ``Client`` or `None`
    """
    index = 0
    limit = len(clients)
    
    while True:
        if index == limit:
            yield None
            return
        
        client = clients[index]
        if client.intents&flag_mask:
            yield client
            break
        
        index += 1
        continue
        
    yield client
    index += 1
    
    while True:
        if index == limit:
            return
        
        client = clients[index]
        if client.intents&flag_mask:
            yield client
        
        index += 1
        continue

def filter_clients_or_me(clients, flag_mask, me):
    """
    Filters the clients whether their intents allow the specific flag. This filter is used, when the clients receive
    the respective event for themselves even if they have the intent disabled.
    
    First yields the first client from `clients` what allows the specified flag.
    
    If non of the clients allow it, then yields `me` (so the source client), what received the event, then expects
    a `user` to be yielded back. At the end when the generator is iterated over inside of a for loop, then it yields
    `me` again (expect if `me` is not the same as the back yielded `user`, but that should not happen, but making sure).
    
    If any of the source clients allow the specified intent flag, then yields the first client what allows it.
    If not the correct client was yielded back, then the generator should be closed. Meanwhile if the correct client
    was yielded, then the generator expects a `user` to be yielded back. After it, the generator is used inside
    of a for loop yielding all the clients from `clients` which allow the specified intent flag including the firstly
    yielded one. At the end yields the received `user` if it is type ``Client`` and it's specified intent flag is not
    allowed.
    
    This function is a generator.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        The clients to filter.
    flag_shift : `int`
        The intent flag's mask based on what the clients will be filtered.
    me : ``Client``
        The source client, what received the respective event.
    
    Yields
    -------
    client : ``Client`` or `None`
    """
    index = 0
    limit = len(clients)
    
    while True:
        if index == limit:
            # If non of the clients have the intent, then yield `me`
            user = yield me
            yield
            if user is me:
                yield me
            return
        
        client = clients[index]
        if client.intents&flag_mask:
            user = yield client
            break
        
        index += 1
        continue
    
    yield
    
    yield client
    index += 1
    
    while True:
        if index == limit:
            break
        
        client = clients[index]
        if client.intents&flag_mask:
            yield client
        
        index += 1
        continue
    
    # Whether the user is type Client and we did not yield it, yield it.
    if not isinstance(user, Client):
        return
    
    if user.intents&flag_mask:
        return
    
    yield user


def filter_just_me(me):
    """
    Yields the source client.
    
    This filter is used when the client itself is the only one who should handle the respective event.
    
    Parameters
    ----------
    me : ``Client``
        The client to yield back.
    
    Yields
    -------
    client : ``Client``
    """
    yield me


def first_client(clients, flag_mask):
    """
    Returns the first client what allows the specified intent flag. If no client allows it, then returns `None`.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    flag_mask : `int`
        The intent flag's mask based on what the clients will be filtered.
    
    Returns
    -------
    client : ``Client`` or `None`
    """
    index = 0
    limit = len(clients)
    
    while True:
        if index == limit:
            return None
        
        client = clients[index]
        if client.intents&flag_mask:
            return client
            break
        
        index += 1
        continue


def first_client_or_me(clients, flag_mask, me):
    """
    Returns the first client what allows the specified intent flag. If non of the clients allow it, then returns `me`.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    flag_mask : `int`
        The intent flag's mask based on what the clients will be filtered.
    me : ``Client``
        The source client, what received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    index = 0
    limit = len(clients)
    
    while True:
        if index == limit:
            return me
        
        client = clients[index]
        if client.intents&flag_mask:
            return client
            break
        
        index += 1
        continue
