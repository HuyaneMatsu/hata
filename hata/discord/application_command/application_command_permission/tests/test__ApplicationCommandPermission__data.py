import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..application_command_permission import ApplicationCommandPermission

from .test__ApplicationCommandPermission__constructor import _asert_fields_set


def test__ApplicationCommandPermission__from_data():
    """
    Tests whether ``ApplicationCommandPermission.from_data`` works as intended.
    """
    application_command_id = 202302220003
    application_id = 202302220004
    guild_id = 202302220005
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220006),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220007),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    data = {
        'id': str(application_command_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'permissions': [overwrite.to_data() for overwrite in permission_overwrites],
    }
    
    application_command_permission = ApplicationCommandPermission.from_data(data)
    _asert_fields_set(application_command_permission)
    
    vampytest.assert_eq(application_command_permission.application_command_id, application_command_id)
    vampytest.assert_eq(application_command_permission.application_id, application_id)
    vampytest.assert_eq(application_command_permission.guild_id, guild_id)
    vampytest.assert_eq(application_command_permission.permission_overwrites, tuple(permission_overwrites))


def test__ApplicationCommandPermission__to_data():
    """
    Tests whether ``ApplicationCommandPermission.to_data`` works as intended.
    
    Case: include defaults
    """
    application_command_id = 202302220008
    application_id = 202302220009
    guild_id = 202302220010
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220011),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220012),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    application_command_permission.application_id = application_id
    application_command_permission.guild_id = guild_id
  
    vampytest.assert_eq(
        application_command_permission.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'id': str(application_command_id),
            'application_id': str(application_id),
            'guild_id': str(guild_id),
            'permissions': [overwrite.to_data(defaults = True) for overwrite in permission_overwrites],
        },
    )
