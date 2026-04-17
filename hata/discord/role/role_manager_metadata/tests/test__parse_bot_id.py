import vampytest

from ..fields import parse_bot_id


def test__parse_bot_id():
    """
    Tests whether ``parse_bot_id`` works as intended.
    """
    bot_id = 202212160001
    
    for input_data, expected_output in (
        ({}, 0),
        ({'bot_id': None}, 0),
        ({'bot_id': str(bot_id)}, bot_id),
    ):
        output = parse_bot_id(input_data)
        vampytest.assert_eq(output, expected_output)
