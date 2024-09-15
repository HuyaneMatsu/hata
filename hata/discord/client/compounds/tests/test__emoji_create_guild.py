import vampytest

from ....emoji import Emoji
from ....guild import Guild
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__emoji_create_guild__stuffed():
    """
    Tests whether ``Client.emoji_create_guild`` works as intended.
    
    Case: stuffed emoji.
    
    This function is a coroutine.
    """
    client_id = 202407270000
    guild_id = 202407270001
    emoji_id = 202407270002
    
    
    mock_api_emoji_create_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
    name = 'OrinGang'
    role_ids = [202407270003, 202407270004]
    reason = 'miau'
    image = IMAGE_DATA
    
    expected_emoji_data = {
        'name': name,
        'roles': [str(role_id) for role_id in role_ids],
        'image': image_to_base64(image),
    }
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
        'roles': [str(role_id) for role_id in role_ids],
    }
    
    
    async def mock_api_emoji_create_guild(input_guild_id, input_emoji_data, input_reason):
        nonlocal mock_api_emoji_create_guild_called
        nonlocal guild_id
        nonlocal expected_emoji_data
        nonlocal output_emoji_data
        nonlocal reason
        nonlocal emoji_id
        mock_api_emoji_create_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(expected_emoji_data, input_emoji_data)
        vampytest.assert_eq(reason, input_reason)
        return output_emoji_data
    
    api.emoji_create_guild = mock_api_emoji_create_guild
        
    try:
        output = await client.emoji_create_guild(
            guild,
            image,
            name = name,
            role_ids = role_ids,
            reason = reason,
        )
        vampytest.assert_true(mock_api_emoji_create_guild_called)
        
        vampytest.assert_instance(output, Emoji)
        vampytest.assert_eq(output.id, emoji_id)
        vampytest.assert_eq(output.guild_id, guild_id)
        vampytest.assert_eq(output.name, name)
        vampytest.assert_eq(output.role_ids, tuple(role_ids))
        
        # It should not be registered, just returned
        vampytest.assert_is(guild.emojis.get(emoji_id, None), None)
    finally:
        client._delete()
        client = None
