__all__ = ()

from ....permission import Permission
from ....permission.constants import PERMISSION_ALLOW_KEY


def parse_allow(data):
    """
    Parses the `allow` field of ``PermissionOverwrite`` out of the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Permission overwrite data.
    
    Returns
    -------
    allow : ``Permission``
    """
    return Permission(data[PERMISSION_ALLOW_KEY])


def validate_allow(allow):
    """
    Validates `allow` field of ``PermissionOverwrite``.
    
    Parameters
    ----------
    allow : `None`, ``Permission``, `int`
        The permission overwrite's allowed permission's value.
    
    Returns
    -------
    allow : ``Permission``
    
    Raises
    ------
    TypeError
        - If `allow` is not `None`, `int`, ``Permission``.
    """
    if allow is None:
        allow = Permission()
    
    elif isinstance(allow, Permission):
        pass
    
    elif isinstance(allow, int):
        allow = Permission(allow)
    
    else:
        raise TypeError(
            f'`allow` can be `None`, `{Permission.__name__}`, `int`, got {allow.__class__.__name__}; {allow!r}.'
        )
    
    return allow


def put_allow_into(allow, data, defaults):
    """
    Puts the `allow` field of ``PermissionOverwrite`` to the given data.
    
    Parameters
    ----------
    allow : ``Permission``
        The permission overwrite's allowed permission's value.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data[PERMISSION_ALLOW_KEY] = format(allow, 'd')
    
    return data
