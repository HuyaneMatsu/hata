__all__ = ()

from ...channel import Channel
from ...role import Role
from ...user import ClientUserBase

from .preinstanced import ApplicationCommandPermissionOverwriteTargetType

APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER = ApplicationCommandPermissionOverwriteTargetType.user
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE = ApplicationCommandPermissionOverwriteTargetType.role
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL = ApplicationCommandPermissionOverwriteTargetType.channel


def validate_application_command_permission_overwrite_target(target):
    """
    Validates the given application command's input target.
    
    Parameters
    ----------
    target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
            ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`, \
            ``ApplicationCommandPermissionOverwriteTargetType``, `int`)), `int`)
        The target entity of the application command permission overwrite.
    
    Returns
    -------
    target_type : ``ApplicationCommandPermissionOverwriteTargetType``
        The target entity's type.
    
    target_id : `int`
        The represented entity's identifier.
    
    Raises
    ------
    TypeError
        - If `target` was not given as any of the expected types & values.
    """
    # GOTO
    while True:
        if isinstance(target, Role):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, ClientUserBase):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, Channel):
            target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
            target_id = target.id
            target_lookup_failed = False
            break
        
        if isinstance(target, tuple) and len(target) == 2:
            target_type_maybe, target_id_maybe = target
            
            if isinstance(target_type_maybe, type):
                if issubclass(target_type_maybe, Role):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                elif issubclass(target_type_maybe, ClientUserBase):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                elif issubclass(target_type_maybe, Channel):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
                else:
                    target_lookup_failed = True
                    break
            
            elif isinstance(target_type_maybe, str):
                if target_type_maybe in ('Role', 'role'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE
                elif target_type_maybe in ('User', 'user'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER
                elif target_type_maybe in ('Channel', 'channel'):
                    target_type = APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL
                else:
                    target_lookup_failed = True
                    break
            
            elif isinstance(target_type_maybe, ApplicationCommandPermissionOverwriteTargetType):
                target_type = target_type_maybe
            
            elif isinstance(target_type_maybe, ApplicationCommandPermissionOverwriteTargetType.VALUE_TYPE):
                target_type = ApplicationCommandPermissionOverwriteTargetType.get(target_type_maybe)
            
            else:
                target_lookup_failed = True
                break
            
            if type(target_id_maybe) is int:
                target_id = target_id_maybe
            elif isinstance(target_id_maybe, int):
                target_id = int(target_id_maybe)
            else:
                target_lookup_failed = True
                break
            
            target_lookup_failed = False
            break
        
        target_lookup_failed = True
        break
    
    if target_lookup_failed:
        raise TypeError(
            f'`target` can be `{Role.__name__}`, `{ClientUserBase.__name__}`, `{Channel.__name__}`, '
            f'`tuple` ((`{Role.__name__}`, `{ClientUserBase.__name__}`, `{Channel.__name__}`, `str` '
            f'(`\'Role\'`, `\'role\'`, `\'User\'`, `\'user\'`, `\'Channel\'`, `\'channel\'`)), `int`), '
            f'got {target.__class__.__name__}: {target!r}.'
        )
    
    return target_type, target_id
