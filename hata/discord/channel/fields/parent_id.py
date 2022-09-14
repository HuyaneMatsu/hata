__all__ = ()

from scarletio import include

from ...bases import maybe_snowflake


Channel = include('Channel')


def parse_parent_id(data):
    """
    Parses out the `parent_id` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    parent_id : `int`
    """
    parent_id = data.get('parent_id', None)
    if (parent_id is None):
        parent_id = 0
    else:
        parent_id = int(parent_id)
    
    return parent_id


def validate_parent_id(parent_id):
    """
    Validates the given `parent_id` field.
    
    Parameters
    ----------
    parent_id : `None`, `str`, `int`, ``Channel``
        The channel's parent's identifier.
    
    Returns
    -------
    parent_id : `int`
    
    Raises
    ------
    TypeError
        - If `parent_id` is not `None`, `str`.
    ValueError
        - If `parent_id` is out of the expected range.
    """
    if parent_id is None:
        processed_parent_id = 0
    
    elif isinstance(parent_id, Channel):
        processed_parent_id = parent_id.id
    
    else:
        processed_parent_id = maybe_snowflake(parent_id)
        if processed_parent_id is None:
            raise TypeError(
                f'`parent_id` can be `int`, `{Channel.__name__}`, `int`, got '
                f'{parent_id.__class__.__name__}; {parent_id!r}.'
            )
    
    return processed_parent_id


def put_parent_id_into(parent_id, data, defaults):
    """
    Puts the `parent_id`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    parent_id : `int`
        The channel's parent's identifier.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if parent_id:
        data['parent_id'] = str(parent_id)
    
    else:
        if defaults:
            data['parent_id'] = None
    
    return data
