__all__ = ()

from ...preconverters import preconvert_bool


def parse_nsfw(data):
    """
    Parses out the `nsfw` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    nsfw : `bool`
    """
    return data.get('nsfw', False)


def validate_nsfw(nsfw):
    """
    Validates the given `nsfw` field.
    
    Parameters
    ----------
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    
    Returns
    -------
    nsfw : `bool`
    
    Raises
    ------
    TypeError
        - If `nsfw` is not `bool`.
    """
    return preconvert_bool(nsfw, 'nsfw')


def put_nsfw_into(nsfw, data, defaults):
    """
    Puts the `nsfw`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if nsfw or defaults:
        data['nsfw'] = nsfw
    
    return data
