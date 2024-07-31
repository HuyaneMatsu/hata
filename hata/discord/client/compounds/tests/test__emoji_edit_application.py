import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_edit_application__stuffed():
    """
    Tests whether ``Client.emoji_edit_application`` works as intended.
    
    Case: stuffed fields.
    
    This function is a coroutine.
    """
    client_id = 202407310003
    emoji_id = 202407310004
    application_id = 202407310005
    
    
    mock_api_emoji_edit_application_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = application_id)
    emoji = Emoji.precreate(emoji_id)
    
    name = 'OrinGang'
    
    expected_emoji_data = {
        'name': name,
    }
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
    }
    
    
    async def mock_api_emoji_edit_application(input_application_id, input_emoji_id, input_emoji_data):
        nonlocal mock_api_emoji_edit_application_called
        nonlocal application_id
        nonlocal emoji_id
        nonlocal expected_emoji_data
        nonlocal output_emoji_data
        mock_api_emoji_edit_application_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        vampytest.assert_eq(expected_emoji_data, input_emoji_data)
        return output_emoji_data
    
    api.emoji_edit_application = mock_api_emoji_edit_application
        
    try:
        output = await client.emoji_edit_application(
            emoji,
            name = name,
        )
        vampytest.assert_true(mock_api_emoji_edit_application_called)
        
        vampytest.assert_is(output, None)
        vampytest.assert_eq(emoji.name, name)
        
        vampytest.assert_eq(client.application._cache_emojis, {emoji_id: emoji})
    finally:
        client._delete()
        client = None
