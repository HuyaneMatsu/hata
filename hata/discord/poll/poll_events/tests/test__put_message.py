import vampytest

from ....message import Message

from ..fields import put_message


def test__put_message__default():
    """
    Tests whether ``put_message`` works as intended.
    """
    message_id = 202404020006
    channel_id = 202404020007
    guild_id = 202404020008
    
    message = Message._create_from_partial_fields(message_id, channel_id, guild_id)
    
    expected_output = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    
    vampytest.assert_eq(
        put_message(message, {}, True),
        expected_output,
    )
