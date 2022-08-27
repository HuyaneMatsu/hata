import vampytest

from ...channel import create_partial_channel_from_id
from ...guild import create_partial_guild_from_id

from .. import Message, MessageFlag


def test__Message__guild_0():
    """
    Tests whether invoking user message's `.guild` can be looked up.
    """
    message_id = 202208270002
    channel_id = 202208270003
    guild_id = 202208270004
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        flags = MessageFlag().update_by_keys(invoking_user_only=True),
    )
    channel = create_partial_channel_from_id(channel_id, -1, guild_id)
    guild = create_partial_guild_from_id(guild_id)
    
    vampytest.assert_is(message.guild, guild)
