import vampytest

from ..fields import validate_target_type
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__validate_target_type__0():
    """
    Validates whether ``validate_target_type`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ApplicationCommandPermissionOverwriteTargetType.role, ApplicationCommandPermissionOverwriteTargetType.role),
        (
            ApplicationCommandPermissionOverwriteTargetType.role.value,
            ApplicationCommandPermissionOverwriteTargetType.role,
        )
    ):
        output = validate_target_type(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_target_type__1():
    """
    Validates whether ``validate_target_type`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_type(input_value)
