__all__ = ()

from scarletio import include

from ....bases import maybe_snowflake

from ..preinstanced import PermissionOverwriteTargetType


Role = include('Role')
ClientUserBase = include('ClientUserBase')


def validate_target(target):
    """
    Validates the `target` field of ``PermissionOverwrite``. target is a mixed representation of `target_id` and
    `target_type`.
    
    Parameters
    ----------
    target : ``Role``, ``ClientUserBase``, `int`
        The permission overwrite's target or it's identifier.
    
    Returns
    -------
    target_id : `int`
        The permission overwrite target's identifier.
    target_type : ``PermissionOverwriteTargetType``
        The permission overwrite's type.
    
    Raises
    ------
    TypeError
        - If `target`'s type is unexpected.
    """
    # target_id
    if isinstance(target, Role):
        target_id = target.id
        target_type = PermissionOverwriteTargetType.role
    
    elif isinstance(target, ClientUserBase):
        target_id = target.id
        target_type = PermissionOverwriteTargetType.user
    
    else:
        target_id = maybe_snowflake(target)
        if (target_id is None):
            raise TypeError(
                f'`target` can be `int`, `{Role.__name__}`, `{ClientUserBase.__name__}`, got '
                f'{target.__class__.__name__}; {target!r}.'
            )
        
        target_type = PermissionOverwriteTargetType.unknown
    
    return target_id, target_type


def put_target_into(target, data, defaults, *, include_internals = False):
    """
    Puts the `target` field of ``PermissionOverwrite`` to the given data.
    
    The `target` value must come from ``validate_target``.
    
    Parameters
    ----------
    target : `tuple` (`int`, ``PermissionOverwriteTargetType``)
        Permission overwrite `target-id`, `target_type` pair.
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
    target_id, target_type = target
    
    if include_internals:
        data['id'] = str(target_id)
    
    if (target_type is not PermissionOverwriteTargetType.unknown):
        data['type'] = target_type.value
    
    return data
