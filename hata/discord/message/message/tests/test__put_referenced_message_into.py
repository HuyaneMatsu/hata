import vampytest

from ..fields import put_referenced_message_into
from ..message import Message
from ..preinstanced import MessageType


@vampytest.skip_if(hasattr(Message, '_fields'))
def test__put_referenced_message_into():
    """
    Tests whether ``put_referenced_message_into`` works as intended.
    """
    message_id_0 = 202305010029
    channel_id_0 = 202305010030
    guild_id_0 = 202305010031
    content_0 = 'Rot in hell'
    
    message_id_1 = 202305010032
    channel_id_1 = 202305010033
    guild_id_1 = 202305010034
    content_1 = 'Afraid'
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id_0,
        content = content_0,
    )
    
    message_1 = Message.precreate(
        message_id_1,
        channel_id = channel_id_1,
        guild_id = guild_id_1,
        content = content_1,
        referenced_message = message_0
    )
    
    for input_value, defaults, recursive, message_type, expected_output in (
        (
            None,
            False,
            False,
            MessageType.default,
            {},
        ), (
            None,
            True,
            True,
            MessageType.default,
            {},
        ), (
            message_0,
            False,
            False,
            MessageType.default,
            {'message_reference': message_0.to_message_reference_data()},
        ), (
            message_0,
            False,
            True,
            MessageType.inline_reply,
            {
                'message_reference': message_0.to_message_reference_data(),
                'referenced_message': message_0.to_data(include_internals = True, recursive = True),
            },
        ), (
            message_1,
            False,
            False,
            MessageType.default,
            {'message_reference': message_1.to_message_reference_data()},
        ), (
            message_1,
            False,
            False,
            MessageType.inline_reply,
            {'message_reference': message_1.to_message_reference_data()},
        ), (
            message_1,
            False,
            True,
            MessageType.inline_reply,
            {
                'message_reference': message_1.to_message_reference_data(),
                'referenced_message': message_1.to_data(include_internals = True, recursive = True),
            },
        )
    ):
        output = put_referenced_message_into(
            input_value, {}, defaults, recursive = recursive, message_type = message_type
        )
        vampytest.assert_eq(output, expected_output)
