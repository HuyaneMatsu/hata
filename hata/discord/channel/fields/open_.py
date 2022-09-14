__all__ = ()

from ...preconverters import preconvert_bool


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


def validate_open(open_):
    """
    Validates the given `open` field.
    
    Parameters
    ----------
    open_ : `bool`
        Whether the channel is open.
    
    Returns
    -------
    open_ : `bool`
    
    Raises
    ------
    TypeError
        - If `open` is not `bool`.
    """
    return preconvert_bool(open_, 'open')


def put_open_into(open_, data, defaults):
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
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if (not open_) or defaults:
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        sub_data['locked'] = not open_
    
    return data
