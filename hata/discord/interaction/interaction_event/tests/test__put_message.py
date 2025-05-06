import vampytest

from ....message import Message

from ..fields import put_message


def test__put_message():
    """
    Tests whether ``put_message`` works as intended.
    """
    message_id = 202210280006
    channel_id = 202210280015
    message = Message.precreate(message_id, channel_id = channel_id)
    
    for input_value, expected_output in (
        (None, {}),
        (message, {'message': message.to_data(include_internals = True)}),
    ):
        output = put_message(input_value, {}, False)
        vampytest.assert_eq(output, expected_output)
