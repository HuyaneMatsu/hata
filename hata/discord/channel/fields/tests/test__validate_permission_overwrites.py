import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..permission_overwrites import validate_permission_overwrites


def test__validate_permission_overwrites__0():
    """
    Tests whether ``validate_permission_overwrites`` works as intended.
    
    Case: passing.
    """
    permission_overwrite = PermissionOverwrite(202209140018, target_type = PermissionOverwriteTargetType.user)
    
    for input_parameter, expected_output in (
        (None, {}),
        ([], {}),
        ([permission_overwrite], {permission_overwrite.target_id: permission_overwrite})
    ):
        output = validate_permission_overwrites(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_permission_overwrites__1():
    """
    Tests whether ``validate_permission_overwrites`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_permission_overwrites(input_parameter)
