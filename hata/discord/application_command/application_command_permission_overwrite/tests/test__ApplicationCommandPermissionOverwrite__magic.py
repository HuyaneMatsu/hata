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


def test__ApplicationCommandPermissionOverwrite__sort():
    """
    Tests whether ``ApplicationCommandPermissionOverwrite`` sort as intended.
    """
    entity_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302210014),
    )
    entity_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302210015),
    )
    entity_2 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.channel, 202302210016),
    )
    entity_3 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302210017),
    )
    entity_4 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302210018),
    )
    entity_5 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.channel, 202302210019),
    )
    
    input = [
        entity_0,
        entity_1,
        entity_2,
        entity_3,
        entity_4,
        entity_5,
    ]
    
    expected_output = [
        entity_0,
        entity_3,
        entity_1,
        entity_4,
        entity_2,
        entity_5,
    ]
    
    vampytest.assert_eq(sorted(input), expected_output)
