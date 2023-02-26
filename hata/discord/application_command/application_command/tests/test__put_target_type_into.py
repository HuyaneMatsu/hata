import vampytest

from ..fields import put_target_type_into
from ..preinstanced import ApplicationCommandTargetType


def test__put_target_type_into():
    """
    Tests whether ``put_target_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (
            ApplicationCommandTargetType.user,
            False,
            {'type': ApplicationCommandTargetType.user.value},
        ),
    ):
        data = put_target_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
