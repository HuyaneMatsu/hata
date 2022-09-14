__all__ = ()


def parse_position(data):
    """
    Parses out the `position` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    position : `int`
    """
    return data.get('position', 0)


def validate_position(position):
    """
    Validates the given `position` field.
    
    Parameters
    ----------
    position : `int`
        The channel's position.
    
    Returns
    -------
    position : `int`
    
    Raises
    ------
    TypeError
        - If `position` is not `int`.
    ValueError
        - If `position` is negative.
    """
    if not isinstance(position, int):
        raise TypeError(
            f'`position` can be `int`, got {position.__class__.__name__}; {position!r}.'
        )
    
    if (position < 0):
        raise ValueError(
            f'`position` cannot be negative, got {position!r}.'
        )
    
    return position


def put_position_into(position, data, defaults):
    """
    Puts the `position`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    position : `int`
        The channel's position.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['position'] = position
    
    return data
