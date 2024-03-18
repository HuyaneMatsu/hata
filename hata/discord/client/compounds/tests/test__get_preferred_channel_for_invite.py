import vampytest

from ....channel import Channel, ChannelType, PermissionOverwrite, PermissionOverwriteTargetType
from ....guild import Guild
from ....permission import Permission
from ....user import GuildProfile

from ...client import Client

from ..invite import _get_preferred_channel_for_invite, _iter_channels_in_preference_order


def _iter_options__iter_channels_in_preference_order():
    guild_id = 202409200008
    channel_id_category = 202409200007
    
    channel_0 = Channel.precreate(
        202409200002, channel_type = ChannelType.guild_text, position = 2, guild_id = guild_id
    )
    channel_1 = Channel.precreate(
        202409200003, channel_type = ChannelType.guild_text, position = 3, guild_id = guild_id
    )
    channel_2 = Channel.precreate(
        202409200004, channel_type = ChannelType.guild_text, position = 4, guild_id = guild_id
    )
    channel_3 = Channel.precreate(
        202409200005,
        channel_type = ChannelType.guild_text,
        parent_id = channel_id_category,
        position = 1,
        guild_id = guild_id,
    )
    channel_4 = Channel.precreate(
        202409200006,
        channel_type = ChannelType.guild_voice,
        parent_id = channel_id_category,
        position = 2,
        guild_id = guild_id,
    )
    channel_5 = Channel.precreate(
        channel_id_category, channel_type = ChannelType.guild_category, position = 1, guild_id = guild_id
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [
            channel_0,
            channel_1,
            channel_2,
            channel_3,
            channel_4,
            channel_5,
        ],
        rules_channel_id = channel_1.id,
        system_channel_id = channel_3.id,
        widget_channel_id = channel_0.id,
    )
    
    yield (
        guild,
        [
            channel_1,
            channel_3,
            channel_0,
            channel_0,
            channel_1,
            channel_2,
            channel_3,
            channel_4,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_channels_in_preference_order()).returning_last())
def test__iter_channels_in_preference_order(guild):
    """
    tests whether ``_iter_channels_in_preference_order`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to iter its channel of.
    
    Returns
    -------
    output : `list<Channel>`
    """
    return [*_iter_channels_in_preference_order(guild)]


def test__get_preferred_channel_for_invite():
    """
    tests whether ``_get_preferred_channel_for_invite`` works as intended.
    """
    guild_id = 202409200012
    client_id = 202409200013
    
    channel_0 = Channel.precreate(202409200009, channel_type = ChannelType.guild_text, guild_id = guild_id)
    channel_1 = Channel.precreate(
        202409200010,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        permission_overwrites = [
            PermissionOverwrite(
                client_id,
                target_type = PermissionOverwriteTargetType.user,
                allow = Permission().update_by_keys(create_instant_invite = True, view_channel = True),
            ),
        ],
    )
    channel_2 = Channel.precreate(202409200011, channel_type = ChannelType.guild_text, guild_id = guild_id)
    
    guild = Guild.precreate(guild_id)
    
    def iter_channels_mock(guild_parameter):
        nonlocal channel_0
        nonlocal channel_1
        nonlocal channel_2
        nonlocal guild
        
        vampytest.assert_is(guild_parameter, guild)
        
        yield channel_0
        yield channel_1
        yield channel_2
    
    mocked = vampytest.mock_globals(
        _get_preferred_channel_for_invite, _iter_channels_in_preference_order = iter_channels_mock
    )
    
    
    client = Client(
        token = 'token_20240920_0000',
        client_id = client_id,
    )
    try:
        guild.clients.append(client)
        client.guilds.add(guild)
        client.guild_profiles[guild.id] = GuildProfile()
    
        output = mocked(client, guild)
        
        vampytest.assert_is(output, channel_1)
    finally:
        client._delete()
        client = None
