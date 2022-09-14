__all__ = ()

from ...preconverters import preconvert_str

from ..constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN


def parse_name(data):
    """
    Parses out the `name` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    name : `str`
    """
    name = data.get('name', None)
    if (name is None):
        name = ''
    
    return name


def validate_name(name):
    """
    Validates the given `name` field.
    
    Parameters
    ----------
    name : `None`, `str`
        Slowmode applied for created threads in the channel.
    
    Returns
    -------
    name : `str`
    
    Raises
    ------
    TypeError
        - If `name` is not `None`, `str`.
    ValueError
        - If `name`'s length out of the expected range.
    """
    if (name is None):
        name = ''
    else:
        name = preconvert_str(name, 'name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)
    
    return name


def put_name_into(name, data, defaults):
    """
    Puts the `name`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    name : `None`, `str`
        The channel's name.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['name'] = name
    
    return data
