import vampytest

from ..application_command_permission_overwrite import ApplicationCommandPermissionOverwrite
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__ApplicationCommandPermissionOverwrite__repr():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.__repr__`` works as intended.
    """
    allow = True
    target_id = 202302210003
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
    
    vampytest.assert_instance(repr(application_command_permission_overwrite), str)


def test__ApplicationCommandPermissionOverwrite__hash():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.__hash__`` works as intended.
    """
    allow = True
    target_id = 202302210004
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
    
    vampytest.assert_instance(hash(application_command_permission_overwrite), int)


def test__ApplicationCommandPermissionOverwrite__eq():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.__eq__`` works as intended.
    """
    allow = True
    target_id = 202302210005
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    keyword_parameters = {
        'allow': allow,
        'target': (target_type, target_id),
    }
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(**keyword_parameters)
    
    vampytest.assert_eq(application_command_permission_overwrite, application_command_permission_overwrite)
    vampytest.assert_ne(application_command_permission_overwrite, object())
    
    for field_name, field_value in (
        ('allow', False),
        ('target', (target_type, 202302210006)),
        ('target', (ApplicationCommandPermissionOverwriteTargetType.channel, target_id)),
    ):
        test_select_option = ApplicationCommandPermissionOverwrite(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(application_command_permission_overwrite, test_select_option)
