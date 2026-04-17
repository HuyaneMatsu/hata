import vampytest

from ..fields import put_self_deaf


def test__put_self_deaf():
    """
    Tests whether ``put_self_deaf`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'self_deaf': False}),
        (False, True, {'self_deaf': False}),
        (True, False, {'self_deaf': True}),
    ):
        data = put_self_deaf(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
