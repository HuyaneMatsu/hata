import vampytest

from ..fields import put_flags_into
from ..flags import UserFlag


def test__put_flags_into():
    """
    Tests whether ``put_flags_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (UserFlag(0), False, {'public_flags': 0}),
        (UserFlag(0), True, {'public_flags': 0}),
        (UserFlag(1), False, {'public_flags': 1}),
    ):
        data = put_flags_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
