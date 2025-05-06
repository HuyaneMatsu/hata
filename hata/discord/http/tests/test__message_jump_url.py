import vampytest

from ...message import Message

from ..urls import DISCORD_ENDPOINT, message_jump_url


def _iter_options():
    guild_id = 202504160000
    channel_id = 202504160001
    
    message_id = 202504160002
    yield (
        guild_id,
        channel_id,
        message_id,
        f'{DISCORD_ENDPOINT}/channels/{guild_id}/{channel_id}/{message_id}',
    )
    
    message_id = 202504160003
    yield (
        0,
        channel_id,
        message_id,
        f'{DISCORD_ENDPOINT}/channels/@me/{channel_id}/{message_id}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__message_jump_url(guild_id, channel_id, message_id):
    """
    Tests whether ``message_jump_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create message with.
    
    channel_id : `int`
        Channel identifier to create message with.
    
    message_id : `int`
        Message identifier to create message with.
    
    Returns
    -------
    output : `str`
    """
    message = Message.precreate(message_id, channel_id = channel_id, guild_id = guild_id)
    
    output = message_jump_url(message)
    
    vampytest.assert_instance(output, str)
    
    return output
