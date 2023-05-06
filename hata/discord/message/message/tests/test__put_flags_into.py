import vampytest

from ..fields import put_flags_into
from ..flags import MessageFlag


def test__put_flags_into():
    """
    Tests whether ``put_flags_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (MessageFlag(0), False, {}),
        (MessageFlag(0), True, {'flags': 0}),
        (MessageFlag(1), False, {'flags': 1}),
    ):
        data = put_flags_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
