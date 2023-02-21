import vampytest

from ..fields import parse_target_type
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__parse_target_type():
    """
    Tests whether ``parse_target_type`` works as intended.
    """
    for input_value, expected_output in (
        (
            {'type': ApplicationCommandPermissionOverwriteTargetType.role.value},
            ApplicationCommandPermissionOverwriteTargetType.role,
        ), (
            {},
            ApplicationCommandPermissionOverwriteTargetType.none,
        ),
    ):
        output = parse_target_type(input_value)
        vampytest.assert_instance(output, ApplicationCommandPermissionOverwriteTargetType)
        vampytest.assert_eq(output, expected_output)
