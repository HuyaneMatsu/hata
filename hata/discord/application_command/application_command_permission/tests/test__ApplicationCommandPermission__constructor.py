import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..application_command_permission import ApplicationCommandPermission


def _asert_fields_set(application_command_permission):
    """
    Checks whether all attributes of the string select option are set.
    
    Parameters
    ----------
    application_command_permission : ``ApplicationCommandPermission.__new__``
        The string select option to check
    """
    vampytest.assert_instance(application_command_permission, ApplicationCommandPermission)
    
    vampytest.assert_instance(application_command_permission.application_command_id, int)
    vampytest.assert_instance(application_command_permission.application_id, int)
    vampytest.assert_instance(application_command_permission.guild_id, int)
    vampytest.assert_instance(application_command_permission.permission_overwrites, tuple, nullable = True)


def test__ApplicationCommandPermission__new():
    """
    Tests whether ``ApplicationCommandPermission.__new__`` works as intended.
    """
    application_command_id = 202302220000
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220001),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220002),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    _asert_fields_set(application_command_permission)
    
    vampytest.assert_eq(application_command_permission.application_command_id, application_command_id)
    vampytest.assert_eq(application_command_permission.permission_overwrites, tuple(permission_overwrites))
