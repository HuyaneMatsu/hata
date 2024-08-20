import vampytest

from ....guild import Guild
from ....user import User, VoiceState

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__voice_state_get__stuffed():
    """
    Tests whether ``Client.voice_state_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202408120000
    guild_id = 202408120001
    user_id = 202408120002
    channel_id = 202408120003
    
    
    mock_api_voice_state_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id)
    
    
    output_user_data = {
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    async def mock_api_voice_state_get(input_guild_id, input_user_id):
        nonlocal mock_api_voice_state_get_called
        nonlocal guild_id
        nonlocal user_id
        nonlocal output_user_data
        mock_api_voice_state_get_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(user_id, input_user_id)
        return output_user_data
    
    api.voice_state_get = mock_api_voice_state_get
        
    try:
        output = await client.voice_state_get(
            guild,
            user,
            force_update = True,
        )
        vampytest.assert_true(mock_api_voice_state_get_called)
        
        vampytest.assert_instance(output, VoiceState)
        vampytest.assert_eq(output.user_id, user_id)
        vampytest.assert_is(output.guild_id, guild_id)
        vampytest.assert_eq(output.channel_id, channel_id)
        
        vampytest.assert_is(guild.get_voice_state(user_id), output)
    finally:
        client._delete()
        client = None
