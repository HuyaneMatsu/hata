import vampytest

from ....guild import Guild
from ....user import VoiceState

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__voice_state_get_own__stuffed():
    """
    Tests whether ``Client.voice_state_get_own`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202408120004
    guild_id = 202408120005
    channel_id = 202408120006
    
    
    mock_api_voice_state_get_own_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
    
    output_user_data = {
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'user_id': str(client_id),
    }
    
    async def mock_api_voice_state_get_own(input_guild_id):
        nonlocal mock_api_voice_state_get_own_called
        nonlocal guild_id
        nonlocal output_user_data
        mock_api_voice_state_get_own_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        return output_user_data
    
    api.voice_state_get_own = mock_api_voice_state_get_own
        
    try:
        output = await client.voice_state_get_own(
            guild,
            force_update = True,
        )
        vampytest.assert_true(mock_api_voice_state_get_own_called)
        
        vampytest.assert_instance(output, VoiceState)
        vampytest.assert_eq(output.user_id, client_id)
        vampytest.assert_is(output.guild_id, guild_id)
        vampytest.assert_eq(output.channel_id, channel_id)
        
        vampytest.assert_is(guild.get_voice_state(client_id), output)
    finally:
        client._delete()
        client = None
