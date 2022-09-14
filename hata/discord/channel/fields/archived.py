__all__ = ()

from ...preconverters import preconvert_bool


def parse_archived(data):
    """
    Parses out the `archived` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    archived : `bool`
    """
    try:
        sub_data = data['thread_metadata']
    except KeyError:
        archived = False
    else:
        archived = sub_data.get('archived', False)
    
    return archived


def validate_archived(archived):
    """
    Validates the given `archived` field.
    
    Parameters
    ----------
    archived : `bool`
        Whether the channel is archived.
    
    Returns
    -------
    archived : `bool`
    
    Raises
    ------
    TypeError
        - If `archived` is not `bool`.
    """
    return preconvert_bool(archived, 'archived')


def put_archived_into(archived, data, defaults):
    """
    Puts the `archived`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    archived : `bool`
        Whether the channel is archived.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if archived or defaults:
        try:
            sub_data = data['thread_metadata']
        except KeyError:
            sub_data = {}
            data['thread_metadata'] = sub_data
        
        sub_data['archived'] = archived
    
    return data
