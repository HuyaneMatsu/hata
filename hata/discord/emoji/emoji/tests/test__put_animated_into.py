import vampytest

from ..fields import put_animated_into


def test__put_animated_into():
    """
    Tests whether ``put_animated_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'animated': False}),
        (True, False, {'animated': True}),
    ):
        data = put_animated_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
