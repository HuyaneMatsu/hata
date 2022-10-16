__all__ = ()

from ....field_validators import bool_validator_factory


def parse_open(data):
    """
    Parses out the `open` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
         Channel data.
    
    Returns
    -------
    open_ : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        open_ = True
    else:
        open_ = not sub_data.get('locked', False)
    
    return open_


def put_open_into(open_, data, defaults, *, flatten_thread_metadata = False):
    """
    Puts the `open`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    open_ : `bool`
        Whether the channel is open.
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
    if (not open_) or defaults:
        if flatten_thread_metadata:
            data_to_use = data
        
        else:
            try:
                data_to_use = data['thread_metadata']
            except KeyError:
                data_to_use = {}
                data['thread_metadata'] = data_to_use
        
        data_to_use['locked'] = not open_
    
    return data


validate_open = bool_validator_factory('open')
