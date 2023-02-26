import vampytest

from ..fields import parse_target_type
from ..preinstanced import ApplicationCommandTargetType


def test__parse_target_type():
    """
    Tests whether ``parse_target_type`` works as intended.
    """
    for input_value, expected_output in (
        (
            {'type': ApplicationCommandTargetType.user.value},
            ApplicationCommandTargetType.user,
        ), (
            {},
            ApplicationCommandTargetType.none,
        ),
    ):
        output = parse_target_type(input_value)
        vampytest.assert_instance(output, ApplicationCommandTargetType)
        vampytest.assert_eq(output, expected_output)
