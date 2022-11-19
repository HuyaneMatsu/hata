import vampytest

from ..fields import put_duration_into


def test__put_duration_into():
    """
    Tests whether ``put_duration_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'duration_seconds': 0}),
    ):
        data = put_duration_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
