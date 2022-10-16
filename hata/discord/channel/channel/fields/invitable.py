__all__ = ()

from ....field_validators import bool_validator_factory


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


def put_invitable_into(invitable, data, defaults, *, flatten_thread_metadata = False):
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
    flatten_thread_metadata : `bool` = `False`, Optional (Keyword only)
        Whether the field should be flattened instead of nested.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (not invitable) or defaults:
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['invitable'] = invitable
    
    return data


validate_invitable = bool_validator_factory('invitable')
