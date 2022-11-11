import vampytest

from ....message import Message

from ..fields import parse_message


def test__parse_message():
    """
    Tests whether ``parse_message`` works as intended.
    """
    message_id = 202210280005
    channel_id = 202210280016
    
    message = Message.custom(message_id = message_id, channel_id = channel_id)
    
    for input_value, expected_output in (
        ({}, None),
        ({'message': None}, None),
        ({'message': message.to_data(include_internals = True)}, message),
    ):
        output = parse_message(input_value)
        vampytest.assert_eq(output, expected_output)
