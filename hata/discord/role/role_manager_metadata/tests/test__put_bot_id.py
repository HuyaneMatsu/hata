import vampytest

from ..fields import put_bot_id


def test__put_bot_id():
    """
    Tests whether ``put_bot_id`` works as intended.
    """
    bot_id = 202212160001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'bot_id': None}),
        (bot_id, False, {'bot_id': str(bot_id)}),
    ):
        data = put_bot_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
