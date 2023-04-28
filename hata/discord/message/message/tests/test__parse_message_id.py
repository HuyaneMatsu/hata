import vampytest

from ..fields import parse_message_id


def test__parse_message_id():
    """
    Tests whether ``parse_message_id`` works as intended.
    """
    message_id = 202304270000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'message_id': None}, 0),
        ({'message_id': str(message_id)}, message_id),
        ({'id': None}, 0),
        ({'id': str(message_id)}, message_id),
        ({'message_id': None, 'id': 123}, 0),
        ({'message_id': str(message_id), 'id': 124}, message_id),
    ):
        output = parse_message_id(input_data)
        vampytest.assert_eq(output, expected_output)
