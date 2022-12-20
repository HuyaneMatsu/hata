__all__ = ()

from ....preconverters import preconvert_preinstanced_type

from ..helpers import get_permission_overwrite_key_value
from ..preinstanced import PermissionOverwriteTargetType


def parse_target_type(data):
    """
    Parses out ``PermissionOverwrite.target_type`` from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Permission overwrite data.
    
    Returns
    -------
    target_type : ``PermissionOverwriteTargetType``
    """
    return PermissionOverwriteTargetType.get(get_permission_overwrite_key_value(data))


def validate_target_type(target_type):
    """
    Validates the given `target_type` field of ``PermissionOverwrite``.
    
    Parameters
    ----------
    target_type : ``PermissionOverwriteTargetType``, `int`
        The permission overwrite's target type.
    
    Returns
    -------
    target_type : ``PermissionOverwriteTargetType``
    
    Raises
    ------
    TypeError
        - If `target_type` is not ``PermissionOverwriteTargetType``, `int`,
    """
    return preconvert_preinstanced_type(target_type, 'target_type', PermissionOverwriteTargetType)


def put_target_type_into(target_type, data, defaults):
    """
    Puts the `target` field of ``PermissionOverwrite`` to the given data.
    
    Parameters
    ----------
    target_type : ``PermissionOverwriteTargetType``
        The permission overwrite's target type.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['type'] = target_type.value
    
    return data
