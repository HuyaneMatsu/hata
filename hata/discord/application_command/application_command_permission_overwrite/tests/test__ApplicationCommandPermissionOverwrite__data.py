import vampytest

from ..application_command_permission_overwrite import ApplicationCommandPermissionOverwrite
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType

from .test__ApplicationCommandPermissionOverwrite__constructor import _asert_fields_set


def test__ApplicationCommandPermissionOverwrite__from_data():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.from_data`` works as intended.
    """
    allow = True
    target_id = 202302210001
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    data = {
        'permission': allow,
        'id': str(target_id),
        'type': target_type.value,
    }
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite.from_data(data)
    _asert_fields_set(application_command_permission_overwrite)
    
    vampytest.assert_eq(application_command_permission_overwrite.allow, allow)
    vampytest.assert_eq(application_command_permission_overwrite.target_id, target_id)
    vampytest.assert_is(application_command_permission_overwrite.target_type, target_type)


def test__ApplicationCommandPermissionOverwrite__to_data():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.to_data`` works as intended.
    
    Case: include defaults
    """
    allow = True
    target_id = 202302210002
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
  
    vampytest.assert_eq(
        application_command_permission_overwrite.to_data(
            defaults = True,
        ),
        {
            'permission': allow,
            'id': str(target_id),
            'type': target_type.value,
        },
    )
