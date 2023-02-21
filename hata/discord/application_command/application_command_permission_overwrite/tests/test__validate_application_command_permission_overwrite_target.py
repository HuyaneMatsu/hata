import vampytest

from ....channel import Channel
from ....role import Role
from ....user import User

from ..helpers import validate_application_command_permission_overwrite_target
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__validate_application_command_permission_overwrite_target__0():
    """
    Tests whether ``validate_application_command_permission_overwrite_target`` works as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (Role.precreate(202302200003), (ApplicationCommandPermissionOverwriteTargetType.role, 202302200003),),
        (User.precreate(202302200004), (ApplicationCommandPermissionOverwriteTargetType.user, 202302200004),),
        (Channel.precreate(202302200005), (ApplicationCommandPermissionOverwriteTargetType.channel, 202302200005),),
        ((Role, 202302200006), (ApplicationCommandPermissionOverwriteTargetType.role, 202302200006),),
        ((User, 202302200007), (ApplicationCommandPermissionOverwriteTargetType.user, 202302200007),),
        ((Channel, 202302200008), (ApplicationCommandPermissionOverwriteTargetType.channel, 202302200008),),
        (('Role', 202302200009), (ApplicationCommandPermissionOverwriteTargetType.role, 202302200009),),
        (('User', 202302200010), (ApplicationCommandPermissionOverwriteTargetType.user, 202302200010),),
        (('Channel', 202302200011), (ApplicationCommandPermissionOverwriteTargetType.channel, 202302200011),),
        (('role', 202302200012), (ApplicationCommandPermissionOverwriteTargetType.role, 202302200012),),
        (('user', 202302200013), (ApplicationCommandPermissionOverwriteTargetType.user, 202302200013),),
        (('channel', 202302200014), (ApplicationCommandPermissionOverwriteTargetType.channel, 202302200014),),
        (
            (ApplicationCommandPermissionOverwriteTargetType.role, 202302200015),
            (ApplicationCommandPermissionOverwriteTargetType.role, 202302200015),
        ),
        (
            (ApplicationCommandPermissionOverwriteTargetType.role.value, 202302200016),
            (ApplicationCommandPermissionOverwriteTargetType.role, 202302200016),
        ),

    ):
        output = validate_application_command_permission_overwrite_target(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_application_command_permission_overwrite_target__1():
    """
    Tests whether ``validate_application_command_permission_overwrite_target`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        object(),
        (object(), 202302200017),
        (object, 202302200018),
        ('object', 202302200019),
        (12.6, 202302200020),
    ):
        with vampytest.assert_raises(TypeError):
            validate_application_command_permission_overwrite_target(input_value)
