import vampytest

from ..fields import put_deaf_into


def test__put_deaf_into():
    """
    Tests whether ``put_deaf_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'deaf': False}),
        (False, True, {'deaf': False}),
        (True, False, {'deaf': True}),
    ):
        data = put_deaf_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
