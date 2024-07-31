import vampytest

from ....emoji import Emoji
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__emoji_create_application__stuffed():
    """
    Tests whether ``Client.emoji_create_application`` works as intended.
    
    Case: stuffed emoji.
    
    This function is a coroutine.
    """
    client_id = 202407310000
    emoji_id = 202407310001
    application_id = 202407310002
    
    
    mock_api_emoji_create_application_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = application_id)
    
    name = 'OrinGang'
    image = IMAGE_DATA
    
    expected_emoji_data = {
        'name': name,
        'image': image_to_base64(image),
    }
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
    }
    
    
    async def mock_api_emoji_create_application(input_application_id, input_emoji_data):
        nonlocal mock_api_emoji_create_application_called
        nonlocal application_id
        nonlocal expected_emoji_data
        nonlocal output_emoji_data
        nonlocal emoji_id
        mock_api_emoji_create_application_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(expected_emoji_data, input_emoji_data)
        return output_emoji_data
    
    api.emoji_create_application = mock_api_emoji_create_application
        
    try:
        output = await client.emoji_create_application(
            image,
            name = name,
        )
        vampytest.assert_true(mock_api_emoji_create_application_called)
        
        vampytest.assert_instance(output, Emoji)
        vampytest.assert_eq(output.id, emoji_id)
        vampytest.assert_eq(output.name, name)
        
        vampytest.assert_eq(client.application._cache_emojis, {emoji_id: output})
    finally:
        client._delete()
        client = None
