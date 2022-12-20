__all__ = ('cr_p_permission_overwrite_object', )

import warnings

from scarletio import include

from .constants import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY

PermissionOverwriteTargetType = include('PermissionOverwriteTargetType')
Role = include('Role')


def cr_p_permission_overwrite_object(target, allow, deny):
    """
    Creates a json serializable object representing a ``PermissionOverwrite``.
    
    Deprecated.
    
    Parameters
    ----------
    target : ``ClientUserBase``, ``Role``
        The target entity of the overwrite.
        The allowed permissions by the overwrite.
    deny : `int`
        The denied permission by the overwrite.
    
    Returns
    -------
    permission_overwrite_data : `dict` of (`str`, `Any) items
    """
    warnings.warn(
        (
            f'`{cr_p_permission_overwrite_object}` is deprecated and will be removed in 2023 April. '
            f'Please use `PermissionOverwrite(...).to_data(...)` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )

    if isinstance(target, Role):
        permission_overwrite_target_type = PermissionOverwriteTargetType.role
    else:
        permission_overwrite_target_type = PermissionOverwriteTargetType.user
    
    return {
        PERMISSION_ALLOW_KEY: allow,
        PERMISSION_DENY_KEY: deny,
        'id': target.id,
        'type': permission_overwrite_target_type.value,
    }
