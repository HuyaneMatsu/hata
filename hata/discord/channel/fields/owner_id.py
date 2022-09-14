__all__ = ()

from scarletio import include

from ...bases import maybe_snowflake


ClientUserBase = include('ClientUserBase')


def parse_owner_id(data):
    """
    Parses out the `owner_id` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        channel data.
    
    Returns
    -------
    owner_id : `int`
    """
    owner_id = data.get('owner_id', None)
    if (owner_id is None):
        owner_id = 0
    else:
        owner_id = int(owner_id)
    
    return owner_id


def validate_owner_id(owner_id):
    """
    Validates the given `owner_id` field.
    
    Parameters
    ----------
    owner_id : `None`, `str`, `int`, ``ClientUserBase``
        The user's identifier who created the group or the thread channel.
    
    Returns
    -------
    owner_id : `int`
    
    Raises
    ------
    TypeError
        - If `owner_id` is not `None`, `str`.
    ValueError
        - If `owner_id` is out of the expected range.
    """
    if owner_id is None:
        processed_owner_id = 0
    
    elif isinstance(owner_id, ClientUserBase):
        processed_owner_id = owner_id.id
    
    else:
        processed_owner_id = maybe_snowflake(owner_id)
        if processed_owner_id is None:
            raise TypeError(
                f'`owner_id` can be `int`, `{ClientUserBase.__name__}`, `int`, got '
                f'{owner_id.__class__.__name__}; {owner_id!r}.'
            )
    
    return processed_owner_id


def put_owner_id_into(owner_id, data, defaults):
    """
    Puts the `owner_id`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    owner_id : `int`
        The user's identifier who created the group or the thread channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if owner_id:
        data['owner_id'] = str(owner_id)
    
    else:
        if defaults:
            data['owner_id'] = None
    
    return data
