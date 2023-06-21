__all__ = ()

from scarletio import include

from ..core import APPLICATION_ID_TO_CLIENT

from .intent import INTENT_MASK_DIRECT_MESSAGES, INTENT_MASK_GUILD_MESSAGES, INTENT_MASK_MESSAGE_CONTENT


Client = include('Client')


def filter_clients(clients, flag_mask, me):
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
    me : ``Client``
        The client who received the respective event.
    
    Yields
    -------
    client : ``Client``, `None`
    """
    iterator = iter(clients)
    for client in iterator:
        if client.intents & flag_mask == flag_mask:
            break
    
    else:
        yield me
        yield me
        return
    
    yield client
    yield client
    
    for client in iterator:
        if client.intents & flag_mask == flag_mask:
            yield client



def get_message_enabled_user_ids(message_data):
    """
    Gets the content field enabled user id-s for the given message.
    
    Parameters
    ----------
    message_data : `dict` of (`str`, `object`) items
        Received message data.
    
    Returns
    -------
    enabled_user_ids : `set` of `int`
    """
    enabled_user_ids = set()
    
    try:
        author_data = message_data['author']
    except KeyError:
        application_id = message_data.get('application_id')
        if (application_id is not None):
            application_id = int(application_id)
            
            try:
                client = APPLICATION_ID_TO_CLIENT[application_id]
            except KeyError:
                pass
            else:
                enabled_user_ids.add(client.id)
            
    else:
        user_id = int(author_data['id'])
        enabled_user_ids.add(user_id)
    
    try:
        user_mention_datas = message_data['mentions']
    except KeyError:
        pass
    else:
        for user_mention_data in user_mention_datas:
            user_id = int(user_mention_data['id'])
            enabled_user_ids.add(user_id)
    
    return enabled_user_ids


def filter_content_intent_client(clients, message_data, me):
    """
    Filters the clients who has message content intent.
    
    First yields the first client from `clients` what allows message content. If non, then yields `None`.
    If a `None` or not the expected client was yielded, then the generator should be closed.
    
    If the correct client was yielded, then the generator is used at a for loop yielding all the clients from `clients`
    which allow the specified flag including the firstly yielded one.
    
    This function is a generator.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    message_data : `dict` of (`str`, `object`) items
        Received message data.
    me : ``Client``
        The client who received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    # Fast check for obvious speed reasons.
    if (len(clients) <= 1) or (message_data.get('flags', 0) & (1 << 6)):
        yield me
        yield me
        return
    
    # Check whether any of the clients has the required intent mask
    flag_mask = INTENT_MASK_MESSAGE_CONTENT
    
    if message_data.get('guild_id', None) is None:
        flag_mask |= INTENT_MASK_DIRECT_MESSAGES
    else:
        flag_mask |= INTENT_MASK_GUILD_MESSAGES
    
    enabled_user_ids = get_message_enabled_user_ids(message_data)
    
    iterator = iter(clients)
    for client in iterator:
        if (client.intents & flag_mask == flag_mask) or (client.id in enabled_user_ids):
            break
    
    else:
        yield me
        yield me
        return
    
    yield client
    yield client
    
    for client in iterator:
        if (client.intents & flag_mask == flag_mask) or (client.id in enabled_user_ids):
            yield client


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
    flag_mask : `int`
        The intent flag's mask based on what the clients will be filtered.
    me : ``Client``
        The client who received the respective event.
    
    Yields
    -------
    client : ``Client``, `None`
    """
    iterator = iter(clients)
    for client in iterator:
        if client.intents & flag_mask == flag_mask:
            break
    
    else:
        user = yield me
        yield
        if user is me:
            yield me
        return
    
    user = yield client
    yield
    yield client
    
    for client in iterator:
        if client.intents & flag_mask == flag_mask:
            yield client
    
    # Whether the user is type Client and we did not yield it, yield it.
    if not isinstance(user, Client):
        return
    
    if user.intents & flag_mask == flag_mask:
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


def first_client(clients, flag_mask, me):
    """
    Returns the first client what allows the specified intent flag. If no client allows it, then returns `None`.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    flag_mask : `int`
        The intent flag's mask based on what the clients will be filtered.
    me : ``Client``
        The client who received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    for client in clients:
        if client.intents & flag_mask == flag_mask:
            return client
    
    return me


def first_content_intent_client(clients, message_data, me):
    """
    Returns the first client, who has message content intent for the given message.
    
    If no client allows it, returns the first client.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    message_data : `dict` of (`str`, `object`) items
        Received message data.
    me : ``Client``
        The client who received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    # Fast check for obvious speed reasons.
    if (len(clients) <= 1) or (message_data.get('flags', 0) & (1 << 6)):
        return me
    
    # Check whether any of the clients has the required intent mask
    flag_mask = INTENT_MASK_MESSAGE_CONTENT
    if message_data.get('guild_id', None) is None:
        flag_mask |= INTENT_MASK_DIRECT_MESSAGES
    else:
        flag_mask |= INTENT_MASK_GUILD_MESSAGES
    
    for client in clients:
        if client.intents & flag_mask == flag_mask:
            return client
    
    enabled_user_ids = get_message_enabled_user_ids(message_data)
    for client in clients:
        if client.id in enabled_user_ids:
            return client
    
    return clients[0]


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
        The client who received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    for client in clients:
        if client.intents & flag_mask == flag_mask:
            return client
    
    return me
