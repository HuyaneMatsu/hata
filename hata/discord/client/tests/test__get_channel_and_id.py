import vampytest

from ...channel import Channel, ChannelType
from ...guild import Guild

from ..client import Client
from ..request_helpers import get_channel_and_id


def _iter_options__passing():
    channel_id = 202406020001
    guild_id = 202406020002
    client_id = 202406020003
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel, Channel.is_guild_text, client_id, guild, [channel, guild], (channel, channel_id)
    
    channel_id = 202406020007
    guild_id = 202406020008
    client_id = 0
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel, Channel.is_guild_voice, client_id, guild, [channel, guild], (channel, channel_id)

    channel_id = 202406020009
    guild_id = 202406020010
    client_id = 202406020011
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel, None, client_id, guild, [channel, guild], (channel, channel_id)

    channel_id = 0
    guild_id = 202406020012
    client_id = 0
    channel = Channel(channel_type = ChannelType.guild_text, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel, Channel.is_guild_text, client_id, guild, [channel, guild], (channel, channel_id)

    channel_id = 202406020013
    guild_id = 202406020014
    client_id = 202406020015
    # channel = Channel(channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel_id, Channel.is_guild_text, client_id, guild, [guild], (None, channel_id)
    
    channel_id = 202406020016
    guild_id = 202406020017
    client_id = 202406020018
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel_id, Channel.is_guild_text, client_id, guild, [channel, guild], (channel, channel_id)
    
    channel_id = 202406020019
    guild_id = 202406020020
    client_id = 0
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel_id, Channel.is_guild_voice, client_id, guild, [channel, guild], (channel, channel_id)

    channel_id = 202406020021
    guild_id = 202406020022
    client_id = 202406020023
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel_id, None, client_id, guild, [channel, guild], (channel, channel_id)


def _iter_options__type_error():
    channel_id = 202406020004
    guild_id = 202406020005
    client_id = 202406020006
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel, Channel.is_guild_voice, client_id, guild, [channel, guild]
    
    channel_id = 202406020025
    guild_id = 202406020026
    client_id = 202406020027
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding')
    guild = Guild.precreate(guild_id)
    yield channel_id, Channel.is_guild_voice, client_id, guild, [channel, guild]
    
    yield None, None, 0, None, []

    yield object(), None, 0, None, []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_channel_and_id(channel, type_checker, client_id, guild, extra):
    """
    Tests whether ``get_channel_and_id`` works as intended.
    
    Parameters
    ----------
    channel : ``Channel``, `int`
        The channel, or it's identifier.
    type_checker : `None | FunctionType`
        Type checker for `channel`.
    client_id : `int`
        Client identifier to instance.
    guild : `None | Guild`
        The channel's guild if any.
    extra : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : `(None | Channel, int)`
    
    Raises
    ------
    TypeError
    """
    if client_id:
        client = Client(
            'token_' + str(client_id),
            client_id = client_id,
        )
    
        if (guild is not None):
            guild.clients.append(client)
    
    try:
        output = get_channel_and_id(channel, type_checker)
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        vampytest.assert_instance(output[0], Channel, nullable = True)
        vampytest.assert_instance(output[1], int)
        return output
        
    finally:
        if client_id:
            client._delete()
            client = None
