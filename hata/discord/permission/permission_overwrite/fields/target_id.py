__all__ = ()

from ....bases import maybe_snowflake


def parse_target_id(data):
    """
    Parses out ``PermissionOverwrite.target_id`` from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Permission overwrite data.
    
    Returns
    -------
    target_id : `int`
    """
    return int(data['id'])


def validate_target_id(target_id):
    """
    Validates the `target_id` field of a ``PermissionOverwrite``.
    
    Parameters
    ----------
    target_id : `int`
        The permission overwrite's target's identifier.
    
    Returns
    -------
    target_id : `int`
    
    Raises
    ------
    TypeError
        - If `target_id` is not `int`.
    """
    processed_target_id = maybe_snowflake(target_id)
    if (processed_target_id is None):
        raise TypeError(
            f'`target_id` can be `int`, got {target_id.__class__.__name__}; {target_id!r}.'
        )
    
    return processed_target_id


def put_target_id_into(target_id, data, defaults, *, include_internals = False):
    """
    Puts the `target` field of ``PermissionOverwrite`` to the given data.
    
    Parameters
    ----------
    target_id : `int`
        The permission overwrite's target's identifier.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    include_internals : `bool` = `False`, Optional (Keyword only)
        Whether internal fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if include_internals:
        data['id'] = str(target_id)
    
    return data
