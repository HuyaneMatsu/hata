__all__ = ()

from ...permission import Permission
from ...utils import PERMISSION_DENY_KEY


def parse_deny(data):
    """
    Parses the `deny` field of ``PermissionOverwrite`` out of the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Permission overwrite data.
    
    Returns
    -------
    deny : ``Permission``
    """
    return Permission(data[PERMISSION_DENY_KEY])


def validate_deny(deny):
    """
    Validates `deny` field of ``PermissionOverwrite``.
    
    Parameters
    ----------
    deny : `None`, ``Permission``, `int`
        The permission overwrite's denied permission's value.
    
    Returns
    -------
    deny : ``Permission``
    
    Raises
    ------
    TypeError
        - If `deny` is not `None`, `int`, ``Permission``.
    """
    if deny is None:
        deny = Permission()
    
    elif isinstance(deny, Permission):
        pass
    
    elif isinstance(deny, int):
        deny = Permission(deny)
    
    else:
        raise TypeError(
            f'`deny` can be `None`, `{Permission.__name__}`, `int`, got {deny.__class__.__name__}; {deny!r}.'
        )
    
    return deny


def put_deny_into(deny, data, defaults):
    """
    Puts the `deny` field of ``PermissionOverwrite`` to the given data.
    
    Parameters
    ----------
    deny : ``Permission``
        The permission overwrite's denied permission's value.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data[PERMISSION_DENY_KEY] = format(deny, 'd')
    
    return data
