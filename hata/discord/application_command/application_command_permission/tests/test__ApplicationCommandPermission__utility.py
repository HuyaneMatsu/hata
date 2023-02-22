import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..application_command_permission import ApplicationCommandPermission

from .test__ApplicationCommandPermission__constructor import _asert_fields_set


def test__ApplicationCommandPermission__copy():
    """
    Tests whether ``ApplicationCommandPermission.copy`` works as intended.
    """
    application_command_id = 202302220022
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220023),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220024),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    copy = application_command_permission.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission, copy)
    
    vampytest.assert_eq(application_command_permission, copy)


def test__ApplicationCommandPermission__copy_with__0():
    """
    Tests whether ``ApplicationCommandPermission.copy_with`` works as intended.
    
    Case: no parameters.
    """ 
    application_command_id = 202302220025
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220026),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220027),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    copy = application_command_permission.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission, copy)
    
    vampytest.assert_eq(application_command_permission, copy)


def test__ApplicationCommandPermission__copy_with__1():
    """
    Tests whether ``ApplicationCommandPermission.copy_with`` works as intended.
    
    Case: All field given
    """
    old_application_command_id = 202302220028
    
    old_overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220029),
    )
    old_overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220030),
    )
    old_permission_overwrites = [old_overwrite_0, old_overwrite_1]
    
    new_application_command_id = 202302220031
    
    new_overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220032),
    )
    new_overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220033),
    )
    
    new_permission_overwrites = [new_overwrite_0, new_overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = old_application_command_id,
        permission_overwrites = old_permission_overwrites,
    )
    
    copy = application_command_permission.copy_with(
        application_command_id = new_application_command_id,
        permission_overwrites = new_permission_overwrites,
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission, copy)
    vampytest.assert_eq(copy.application_command_id, new_application_command_id)
    vampytest.assert_eq(copy.permission_overwrites, tuple(new_permission_overwrites))



def test__ApplicationCommandPermission__iter_permission_overwrites():
    """
    Tests whether ``ApplicationCommandPermission.iter_permission_overwrites`` works as intended.
    
    Case: no parameters.
    """ 
    application_command_id = 202302220034
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220035),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220036),
    )
    
    for input_value, expected_output in (
        (None, []),
        ([overwrite_0], [overwrite_0]),
        ([overwrite_0, overwrite_1], [overwrite_0, overwrite_1]),
    ):
        application_command_permission = ApplicationCommandPermission(
            application_command_id = application_command_id,
            permission_overwrites = input_value,
        )
        
        vampytest.assert_eq([*application_command_permission.iter_permission_overwrites()], expected_output)
