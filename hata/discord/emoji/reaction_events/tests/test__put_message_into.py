import vampytest

from ....message import Message

from ..fields import put_message_into


def test__put_message_into__0():
    """
    Tests whether ``put_message_into`` works as intended.
    """
    message_id = 202301020021
    channel_id = 202301020022
    guild_id = 202301020023
    
    message = Message._create_from_partial_fields(message_id, channel_id, guild_id)
    
    expected_output = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    
    vampytest.assert_eq(
        put_message_into(message, {}, True),
        expected_output,
    )
