import vampytest

from ....message import Message

from ..fields import parse_message


def test__parse_message__0():
    """
    Tests whether ``parse_message`` works as intended.
    
    Case: Returns correctly.
    """
    message_id = 202301020015
    channel_id = 202301020016
    guild_id = 202301020017
    
    data = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    
    message = parse_message(data)
    
    vampytest.assert_instance(message, Message)
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)


def test__parse_message__1():
    """
    Tests whether ``parse_message`` works as intended.
    
    Case: Cache.
    """
    message_id = 202301020018
    channel_id = 202301020019
    guild_id = 202301020020
    
    data = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    message = parse_message(data)
    test_message = parse_message(data)
    
    vampytest.assert_is(message, test_message)
