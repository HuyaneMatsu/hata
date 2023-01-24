import vampytest

from ..fields import put_self_deaf_into


def test__put_self_deaf_into():
    """
    Tests whether ``put_self_deaf_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'self_deaf': False}),
        (False, True, {'self_deaf': False}),
        (True, False, {'self_deaf': True}),
    ):
        data = put_self_deaf_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
