import vampytest

from ..fields import put_bot_into


def test__put_bot_into():
    """
    Tests whether ``put_bot_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'bot': False}),
        (False, True, {'bot': False}),
        (True, False, {'bot': True}),
    ):
        data = put_bot_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
