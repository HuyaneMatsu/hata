__all__ = ()

from ...preconverters import preconvert_int

from ..constants import USER_LIMIT_DEFAULT, USER_LIMIT_MAX, USER_LIMIT_MIN


def parse_user_limit(data):
    """
    Parses out the `user_limit` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    user_limit : `int`
    """
    return data.get('user_limit', USER_LIMIT_DEFAULT)


def validate_user_limit(user_limit):
    """
    Validates the given `user_limit` field.
    
    Parameters
    ----------
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Returns
    -------
    user_limit : `int`
    
    Raises
    ------
    TypeError
        - If `user_limit` is not `int`.
    ValueError
        - If `user_limit` is out of the expected range.
    """
    return preconvert_int(user_limit, 'user_limit', USER_LIMIT_MIN, USER_LIMIT_MAX)


def put_user_limit_into(user_limit, data, defaults):
    """
    Puts the `user_limit`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['user_limit'] = user_limit
    
    return data
