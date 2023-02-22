import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..application_command_permission import ApplicationCommandPermission


def test__ApplicationCommandPermission__repr():
    """
    Tests whether ``ApplicationCommandPermission.__repr__`` works as intended.
    """
    application_command_id = 202302220013
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220014),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220015),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    
    vampytest.assert_instance(repr(application_command_permission), str)


def test__ApplicationCommandPermission__hash():
    """
    Tests whether ``ApplicationCommandPermission.__hash__`` works as intended.
    """
    application_command_id = 202302220016
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220017),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220018),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    application_command_permission = ApplicationCommandPermission(
        application_command_id = application_command_id,
        permission_overwrites = permission_overwrites,
    )
    
    vampytest.assert_instance(hash(application_command_permission), int)


def test__ApplicationCommandPermission__eq():
    """
    Tests whether ``ApplicationCommandPermission.__eq__`` works as intended.
    """
    application_command_id = 202302220019
    
    overwrite_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302220020),
    )
    overwrite_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302220021),
    )
    
    permission_overwrites = [overwrite_0, overwrite_1]
    
    keyword_parameters = {
        'application_command_id': application_command_id,
        'permission_overwrites': permission_overwrites,
    }
    
    application_command_permission = ApplicationCommandPermission(**keyword_parameters)
    
    vampytest.assert_eq(application_command_permission, application_command_permission)
    vampytest.assert_ne(application_command_permission, object())
    
    for field_name, field_value in (
        ('application_command_id', False),
        ('permission_overwrites', None)
    ):
        test_select_option = ApplicationCommandPermission(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(application_command_permission, test_select_option)
