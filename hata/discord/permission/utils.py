__all__ = ('get_permission_overwrite_key_value', 'cr_p_overwrite_object', )

from ...env import API_VERSION

from ...backend.export import include

from .preinstanced import PermissionOverwriteTargetType

Role = include('Role')

if API_VERSION in (6, 7):
    PERMISSION_KEY = 'permissions_new'
    PERMISSION_ALLOW_KEY = 'allow_new'
    PERMISSION_DENY_KEY = 'deny_new'
    
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `str`
        """
        return data['type']
else:
    PERMISSION_KEY = 'permissions'
    PERMISSION_ALLOW_KEY = 'allow'
    PERMISSION_DENY_KEY = 'deny'
    
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `int`
        """
        return int(data['type'])


def cr_p_overwrite_object(target, allow, deny):
    """
    Creates a json serializable object representing a ``PermissionOverwrite``(permission overwrite).
    
    Parameters
    ----------
    target : ``ClientUserBase`` or ``Role``
        The target entity of the overwrite.
        The allowed permissions by the overwrite.
    deny : `int`
        The denied permission by the overwrite.
    
    Returns
    -------
    permission_overwrite_data : `dict` of (`str`, `Any) items
    """
    if isinstance(target, Role):
        overwrite_target_type = PermissionOverwriteTargetType.role
    else:
        overwrite_target_type = PermissionOverwriteTargetType.user
    
    return {
        'allow': allow,
        'deny': deny,
        'id': target.id,
        'type': overwrite_target_type.value,
    }
