import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target_type import validate_target_type


def test__validate_target_type__0():
    """
    Tests whether ``validate_target_type`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (PermissionOverwriteTargetType.user, PermissionOverwriteTargetType.user),
        (PermissionOverwriteTargetType.user.value, PermissionOverwriteTargetType.user),
    ):
        output = validate_target_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target_type__1():
    """
    Tests whether ``validate_target_type`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_type(input_value)
