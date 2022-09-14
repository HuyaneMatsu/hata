__all__ = ()

from ...preconverters import preconvert_bool


def parse_invitable(data):
    """
    Parses out the `invitable` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    invitable : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        invitable = True
    else:
        invitable = sub_data.get('invitable', True)
    
    return invitable


def validate_invitable(invitable):
    """
    Validates the given `invitable` field.
    
    Parameters
    ----------
    invitable : `bool`
        Whether non-moderators can invite other non-moderators to the threads.
    
    Returns
    -------
    invitable : `bool`
    
    Raises
    ------
    TypeError
        - If `invitable` is not `bool`.
    """
    return preconvert_bool(invitable, 'invitable')


def put_invitable_into(invitable, data, defaults):
    """
    Puts the `invitable`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    invitable : `bool`
        Whether non-moderators can invite other non-moderators to the threads.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (not invitable) or defaults:
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        sub_data['invitable'] = invitable
    
    return data
