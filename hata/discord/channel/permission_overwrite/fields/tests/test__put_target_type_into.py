import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target_type import put_target_type_into


def test__put_target_type_into():
    """
    Tests whether ``put_target_type_into`` works as intended.
    """
    for input_value, expected_output in (
        (PermissionOverwriteTargetType.user, {'type': PermissionOverwriteTargetType.user.value}),
    ):
        output_data = put_target_type_into(input_value, {}, True)
        vampytest.assert_eq(output_data, expected_output)
