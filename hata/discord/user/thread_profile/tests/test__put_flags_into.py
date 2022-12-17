import vampytest

from ..fields import put_flags_into
from ..flags import ThreadProfileFlag


def test__put_flags_into():
    """
    Tests whether ``put_flags_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ThreadProfileFlag(0), False, {}),
        (ThreadProfileFlag(0), True, {'flags': 0}),
        (ThreadProfileFlag(1), False, {'flags': 1}),
    ):
        data = put_flags_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
