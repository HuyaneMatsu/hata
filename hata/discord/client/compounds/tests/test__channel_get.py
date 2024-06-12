import vampytest

from ....channel import Channel, ChannelType
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__channel_get():
    """
    Tests whether ``Client.channel_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202406020028
    channel_id = 202406020029
    guild_id = 202406020030
    
    mock_api_channel_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    guild.clients.append(client)
    
    channel = Channel.precreate(
        channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id, name = 'pudding'
    )
    new_name = 'sister'
    
    response_data = {
        **channel.to_data(include_internals = True),
        'name': new_name,
    }
    
    async def mock_api_channel_get(input_channel_id):
        nonlocal mock_api_channel_get_called
        nonlocal channel_id
        nonlocal response_data
        
        mock_api_channel_get_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        
        return response_data
    
    
    api.channel_get = mock_api_channel_get
        
    try:
        output = await client.channel_get(channel, force_update = True)
        vampytest.assert_true(mock_api_channel_get_called)
        
        vampytest.assert_is(output, channel)
        vampytest.assert_eq(channel.name, new_name)
    finally:
        client._delete()
        client = None
