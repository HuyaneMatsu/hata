import vampytest

from ..fields import parse_referenced_message
from ..message import Message


def test__parse_referenced_message__0():
    """
    Tests whether ``parse_referenced_message`` works as intended.
    
    Case: Nothing.
    """
    for input_data in (
        {},
        {'referenced_message': None},
        {'message_reference': None},
    ):
        output = parse_referenced_message(input_data)
        vampytest.assert_is(output, None)


def test__parse_referenced_message__1():
    """
    Tests whether ``parse_referenced_message`` works as intended.
    
    Case: Partial.
    """
    message_id = 202305010023
    channel_id = 202305010024
    guild_id = 202305010025
    
    input_data = {
        'message_reference': {
            'message_id': str(message_id),
            'channel_id': str(channel_id),
            'guild_id': str(guild_id),
        }
    }
    
    output = parse_referenced_message(input_data)
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, Message)
    vampytest.assert_eq(output.id, message_id)
    vampytest.assert_eq(output.channel_id, channel_id)
    vampytest.assert_eq(output.guild_id, guild_id)


def test__parse_referenced_message__2():
    """
    Tests whether ``parse_referenced_message`` works as intended.
    
    Case: Full.
    """
    message_id = 202305010026
    channel_id = 202305010027
    guild_id = 202305010028
    content = 'Rot in hell'
    
    input_data = {
        'referenced_message': {
            'content': content,
            'id': str(message_id),
            'channel_id': str(channel_id),
            'guild_id': str(guild_id),
        }
    }
    
    output = parse_referenced_message(input_data)
    vampytest.assert_is_not(output, None)
    vampytest.assert_instance(output, Message)
    vampytest.assert_eq(output.id, message_id)
    vampytest.assert_eq(output.channel_id, channel_id)
    vampytest.assert_eq(output.guild_id, guild_id)
    vampytest.assert_eq(output.content, content)
