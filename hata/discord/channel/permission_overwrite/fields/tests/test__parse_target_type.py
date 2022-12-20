import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target_type import parse_target_type


def test__parse_target_type():
    """
    Tests whether ``parse_target_type`` works as intended.
    """
    for input_value, expected_output in (
        ({'type': PermissionOverwriteTargetType.user.value}, PermissionOverwriteTargetType.user),
    ):
        output = parse_target_type(input_value)
        vampytest.assert_instance(output, PermissionOverwriteTargetType)
        vampytest.assert_eq(output, expected_output)
