__all__ = ()

from ...preconverters import preconvert_int

from ..constants import SLOWMODE_MAX, SLOWMODE_MIN


def parse_slowmode(data):
    """
    Parses out the `slowmode` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    slowmode : `int`
    """
    slowmode = data.get('rate_limit_per_user', None)
    if slowmode is None:
        slowmode = 0
    
    return slowmode


def validate_slowmode(slowmode):
    """
    Validates the given `slowmode` field.
    
    Parameters
    ----------
    slowmode : `int`
        The amount of time in seconds that a user needs to wait between it's each message.
    
    Returns
    -------
    slowmode : `int`
    
    Raises
    ------
    TypeError
        - If `slowmode` is not `int`.
    ValueError
        - If `slowmode` is out of the expected range.
    """
    return preconvert_int(slowmode, 'slowmode', SLOWMODE_MIN, SLOWMODE_MAX)


def put_slowmode_into(slowmode, data, defaults):
    """
    Puts the `slowmode`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    slowmode : `int`
        The amount of time in seconds that a user needs to wait between it's each message.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if slowmode == 0:
        if defaults:
            data['rate_limit_per_user'] = None
    else:
        data['rate_limit_per_user'] = slowmode
    
    return data
