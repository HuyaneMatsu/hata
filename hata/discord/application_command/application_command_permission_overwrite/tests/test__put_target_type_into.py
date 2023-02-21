import vampytest

from ..fields import put_target_type_into
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__put_target_type_into():
    """
    Tests whether ``put_target_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (
            ApplicationCommandPermissionOverwriteTargetType.role,
            False,
            {'type': ApplicationCommandPermissionOverwriteTargetType.role.value},
        ),
    ):
        data = put_target_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
