import vampytest

from ....message import Message

from ..fields import put_messages_into


def test__put_messages_into():
    """
    Tests whether ``put_messages_into`` works as intended.
    """
    message_id = 202211050020
    message_content = 'Faker'
    
    message = Message.precreate(
        message_id,
        content = message_content,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'messages': {}}),
        (
            {
                message_id: message,
            },
                True,
            {
                'messages': {
                    str(message_id): message.to_data(defaults = True, include_internals = True),
                }
            },
        )
    ):
        output = put_messages_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
