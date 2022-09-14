__all__ = ()

from ...permission import PermissionOverwrite


def parse_permission_overwrites(data):
    """
    Parses the permission overwrites from the given data and returns them.
    
    Parameters
    ----------
    data : `list` of (`dict` of (`str`, `Any`) items) elements
        A list of permission overwrites' data.
    
    Returns
    -------
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
    """
    permission_overwrites = {}
    
    permission_overwrites_datas = data.get('permission_overwrites', None)
    if (permission_overwrites_datas is not None) and permission_overwrites_datas:
        for permission_overwrite_data in permission_overwrites_datas:
            permission_overwrite = PermissionOverwrite.from_data(permission_overwrite_data)
            permission_overwrites[permission_overwrite.target_id] = permission_overwrite
    
    return permission_overwrites


def validate_permission_overwrites(permission_overwrites):
    """
    Validates the given `permission_overwrites` field.
    
    Parameters
    ----------
    permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``
        The permission_overwrites to validate.
    
    Returns
    -------
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
    """
    if permission_overwrites is None:
        return {}
    
    if (getattr(permission_overwrites, '__iter__', None) is None):
        raise TypeError(
            f'`permission_overwrites` can be `None`, `iterable` of `{PermissionOverwrite.__name__}`, got '
            f'{permission_overwrites.__class__.__name__}; {permission_overwrites!r}.'
        )
    
    permission_overwrites_processed = {}
    
    for permission_overwrite in permission_overwrites:
        if not isinstance(permission_overwrite, PermissionOverwrite):
            raise TypeError(
                f'`permission_overwrites` can contain `{PermissionOverwrite.__name__}` elements, got '
                f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}; '
                f'permission_overwrites = {permission_overwrites!r}.'
            )
        
        permission_overwrites_processed[permission_overwrite.target_id] = permission_overwrite
    
    return permission_overwrites_processed


def put_permission_overwrites_into(permission_overwrites, data, defaults):
    """
    Puts the `permission_overwrites`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    permission_overwrites :`dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['permission_overwrites'] = [
        permission_overwrite.to_data(include_internals = True)
        for permission_overwrite in permission_overwrites.values()
    ]
    
    return data
