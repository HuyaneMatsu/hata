import vampytest

from ....channel import Channel
from ....role import Role
from ....user import ClientUserBase

from ..application_command_permission_overwrite import ApplicationCommandPermissionOverwrite
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType

from .test__ApplicationCommandPermissionOverwrite__constructor import _asert_fields_set


def test__ApplicationCommandPermissionOverwrite__copy():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.copy`` works as intended.
    """
    allow = True
    target_id = 202302210007
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
    copy = application_command_permission_overwrite.copy()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission_overwrite, copy)
    
    vampytest.assert_eq(application_command_permission_overwrite, copy)


def test__ApplicationCommandPermissionOverwrite__copy_with__0():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.copy_with`` works as intended.
    
    Case: no parameters.
    """ 
    allow = True
    target_id = 202302210008
    target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = allow,
        target = (target_type, target_id)
    )
    copy = application_command_permission_overwrite.copy_with()
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission_overwrite, copy)
    
    vampytest.assert_eq(application_command_permission_overwrite, copy)


def test__ApplicationCommandPermissionOverwrite__copy_with__1():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.copy_with`` works as intended.
    
    Case: All field given
    """
    old_allow = True
    old_target_id = 202302210009
    old_target_type = ApplicationCommandPermissionOverwriteTargetType.role
    
    new_allow = False
    new_target_id = 202302210010
    new_target_type = ApplicationCommandPermissionOverwriteTargetType.channel
    
    application_command_permission_overwrite = ApplicationCommandPermissionOverwrite(
        allow = old_allow,
        target = (old_target_type, old_target_id)
    )
    
    copy = application_command_permission_overwrite.copy_with(
        allow = new_allow,
        target = (new_target_type, new_target_id)
    )
    
    _asert_fields_set(copy)
    vampytest.assert_is_not(application_command_permission_overwrite, copy)
    vampytest.assert_eq(copy.allow, new_allow)
    vampytest.assert_eq(copy.target_id, new_target_id)
    vampytest.assert_is(copy.target_type, new_target_type)


def test__ApplicationCommandPermissionOverwrite__target():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite.target`` works as intended.
    """
    for target_type, target_id, expected_output_type in (
        (ApplicationCommandPermissionOverwriteTargetType.role, 202302210011, Role),
        (ApplicationCommandPermissionOverwriteTargetType.user, 202302210012, ClientUserBase),
        (ApplicationCommandPermissionOverwriteTargetType.channel, 202302210013, Channel),
    ):
        output = ApplicationCommandPermissionOverwrite(
            allow = False,
            target = (target_type, target_id)
        ).target
        
        vampytest.assert_instance(output, expected_output_type)
        vampytest.assert_eq(output.id, target_id)
