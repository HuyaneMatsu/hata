import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_delete_application():
    """
    Tests whether ``Client.emoji_delete_application`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407310006
    emoji_id = 202407310007
    application_id = 202407310008
    
    
    mock_api_emoji_delete_application_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = application_id)
    emoji = Emoji.precreate(emoji_id)
    client.application._add_cache_emoji(emoji)
    
    
    async def mock_api_emoji_delete_application(input_application_id, input_emoji_id):
        nonlocal mock_api_emoji_delete_application_called
        nonlocal application_id
        nonlocal emoji_id
        mock_api_emoji_delete_application_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        return None
    
    api.emoji_delete_application = mock_api_emoji_delete_application
        
    try:
        output = await client.emoji_delete_application(
            emoji,
        )
        vampytest.assert_true(mock_api_emoji_delete_application_called)
        
        vampytest.assert_is(output, None)
        vampytest.assert_eq(client.application._cache_emojis, None)
    finally:
        client._delete()
        client = None
