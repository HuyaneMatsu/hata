import vampytest

from ....message import Message

from ..fields import parse_messages


def test__parse_messages():
    """
    Tests whether ``parse_messages`` works as intended.
    """
    message_id = 202211050019
    message_content = 'Faker'
    
    message = Message.precreate(
        message_id,
        content = message_content,
    )
    
    for input_value, expected_output in (
        ({}, None),
        ({'messages': {}}, None),
        (
            {
                'messages': {
                    str(message_id): message.to_data(defaults = True, include_internals = True),
                }
            },
            {
                message_id: message,
            }
        )
    ):
        output = parse_messages(input_value)
        vampytest.assert_eq(output, expected_output)
