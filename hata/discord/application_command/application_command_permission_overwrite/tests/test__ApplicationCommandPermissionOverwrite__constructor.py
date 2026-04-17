import vampytest

from ..application_command_permission_overwrite import ApplicationCommandPermissionOverwrite
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def _asert_fields_set(application_command_permission_overwrite):
    """
    Checks whether all attributes of the application command permission overwrite.
    
    Parameters
    ----------
    application_command_permission_overwrite : ``ApplicationCommandPermissionOverwrite``
        The application command permission overwrite to check.
    """
    vampytest.assert_instance(application_command_permission_overwrite, ApplicationCommandPermissionOverwrite)
    
    vampytest.assert_instance(application_command_permission_overwrite.allow, bool)
    vampytest.assert_instance(application_command_permission_overwrite.target_id, int)
    vampytest.assert_instance(
        application_command_permission_overwrite.target_type, ApplicationCommandPermissionOverwriteTargetType,
    )


def test__ApplicationCommandPermissionOverwrite__new():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.__new__`` works as intended.
    """
    allow = True
    target_id = 202302210000
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
    _asert_fields_set(application_command_permission_overwrite)
    
    vampytest.assert_eq(application_command_permission_overwrite.allow, allow)
    vampytest.assert_eq(application_command_permission_overwrite.target_id, target_id)
    vampytest.assert_is(application_command_permission_overwrite.target_type, target_type)
