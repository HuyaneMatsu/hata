import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)

from ..fields import validate_permission_overwrites


def test__validate_permission_overwrites__0():
    """
    Tests whether `validate_permission_overwrites` works as intended.
    
    Case: passing.
    """
    entity_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302210032),
    )
    entity_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302210033),
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([entity_0, entity_1], (entity_0, entity_1)),
    ):
        output = validate_permission_overwrites(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_permission_overwrites__2():
    """
    Tests whether `validate_permission_overwrites` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_permission_overwrites(input_value)
