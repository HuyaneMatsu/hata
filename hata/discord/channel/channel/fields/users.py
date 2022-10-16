__all__ = ()

from ....bases import maybe_snowflake
from ....user import ClientUserBase, User, create_partial_user_from_id


def parse_users(data):
    """
    Parses out the `users` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    users : `list` of ``ClientUserBase``
    """
    users = []
    
    try:
        user_datas = data['recipients']
    except KeyError:
        pass
    else:
        for user_data in user_datas:
            user = User.from_data(user_data)
            users.append(user)
        
        users.sort()
    
    return users


def validate_users(users):
    """
    Validates the given `users` field.
    
    Parameters
    ----------
    users : `iterable` of (``ClientUserBase``, `int`)
        The users in the channel.
    
    Returns
    -------
    users : `list` of ``ClientUserBase``
    
    Raises
    ------
    TypeError
        - If `users` is not `list` of (``ClientUserBase``, `int`).
    """
    if (getattr(users, '__iter__', None) is None):
        raise TypeError(
            f'`users` can be `None`, `iterable` of (`int`, `{ClientUserBase.__name__}`), '
            f'got {users.__class__.__name__}; {users!r}.'
        )
    
    users_processed = set()
    
    for user in users:
        if not isinstance(user, ClientUserBase):
            user_id = maybe_snowflake(user)
            if user_id is None:
                raise TypeError(
                    f'`users` can contain `int`, `{ClientUserBase.__name__}` elements, got '
                    f'{user.__class__.__name__}; {user!r}; users={users!r}.'
                )
            
            user = create_partial_user_from_id(user_id)
        
        users_processed.add(user)
    
    return sorted(users_processed)


def put_users_into(users, data, defaults):
    """
    Puts the `users`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    users : `list` of ``ClientUserBase``
        The users in the channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['recipients'] = [user.to_data() for user in users]
    
    return data
