import vampytest

from ..fields import put_oauth2_flags_into
from ..flags import UserFlag


def test__put_oauth2_flags_into():
    """
    Tests whether ``put_oauth2_flags_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (UserFlag(0), False, {'flags': 0}),
        (UserFlag(0), True, {'flags': 0}),
        (UserFlag(1), False, {'flags': 1}),
    ):
        data = put_oauth2_flags_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
