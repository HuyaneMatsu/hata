import vampytest

from ..fields import put_large_into


def test__put_large_into():
    """
    Tests whether ``put_large_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'large': False}),
        (True, False, {'large': True}),
    ):
        data = put_large_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
