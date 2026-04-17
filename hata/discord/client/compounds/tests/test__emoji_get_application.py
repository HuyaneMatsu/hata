import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_get_application__stuffed():
    """
    Tests whether ``Client.emoji_get_application`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407310009
    emoji_id = 202407310010
    application_id = 202407310011
    
    
    mock_api_emoji_get_application_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = application_id)
    emoji = Emoji.precreate(emoji_id)
    
    name = 'OrinGang'
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
    }
    
    async def mock_api_emoji_get_application(input_application_id, input_emoji_id):
        nonlocal mock_api_emoji_get_application_called
        nonlocal application_id
        nonlocal emoji_id
        nonlocal output_emoji_data
        mock_api_emoji_get_application_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        return output_emoji_data
    
    api.emoji_get_application = mock_api_emoji_get_application
        
    try:
        output = await client.emoji_get_application(
            emoji,
            force_update = True,
        )
        vampytest.assert_true(mock_api_emoji_get_application_called)
        
        vampytest.assert_instance(output, Emoji)
        vampytest.assert_eq(output.id, emoji_id)
        vampytest.assert_eq(output.name, name)
        
        vampytest.assert_eq(client.application._cache_emojis, {emoji_id: emoji})
    finally:
        client._delete()
        client = None
