import vampytest

from ..fields import put_flags_into
from ..flags import ActivityFlag


def test__put_flags_into():
    """
    Tests whether ``put_flags_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (ActivityFlag(0), False, {}),
        (ActivityFlag(0), True, {'flags': 0}),
        (ActivityFlag(1), False, {'flags': 1}),
    ):
        data = put_flags_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
