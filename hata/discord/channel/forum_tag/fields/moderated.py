__all__ = ()

from ....preconverters import preconvert_bool


def parse_moderated(data):
    """
    Parses out the `moderated` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    moderated : `bool`
    """
    return data.get('moderated', False)


def validate_moderated(moderated):
    """
    Validates the given `moderated` field.
    
    Parameters
    ----------
    moderated : `bool`
        Whether this tag can only be added or removed by a user with `manage_threads` permission.
    
    Returns
    -------
    moderated : `bool`
    
    Raises
    ------
    TypeError
        - If `moderated` is not `bool`.
    """
    return preconvert_bool(moderated, 'moderated')


def put_moderated_into(moderated, data, defaults):
    """
    Puts the `moderated`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    moderated : `bool`
        Whether this tag can only be added or removed by a user with `manage_threads` permission.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if moderated or defaults:
        data['moderated'] = moderated
    
    return data
