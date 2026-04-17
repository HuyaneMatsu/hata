
import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_get_all_application():
    """
    Tests whether ``Client.emoji_get_all_application`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407310012
    emoji_id_0 = 202407310013
    emoji_id_1 = 202407310014
    application_id = 202407310015
    
    
    mock_api_emoji_get_all_application_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = application_id)
    
    name_0 = 'OrinGang'
    name_1 = 'OrinDance'
    
    output_emoji_datas = {
        'items': [
            {
                'id': str(emoji_id_0),
                'animated': False,
                'name': name_0,
            }, {
                'id': str(emoji_id_1),
                'animated': False,
                'name': name_1,
            },
        ],
    }
    
    async def mock_api_emoji_get_all_application(input_application_id):
        nonlocal mock_api_emoji_get_all_application_called
        nonlocal application_id
        nonlocal output_emoji_datas
        mock_api_emoji_get_all_application_called = True
        vampytest.assert_eq(application_id, input_application_id)
        return output_emoji_datas
    
    api.emoji_get_all_application = mock_api_emoji_get_all_application
        
    try:
        output = await client.emoji_get_all_application()
        vampytest.assert_true(mock_api_emoji_get_all_application_called)
        
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(len(output), 2)
        
        output_emoji_0 = output[0]
        vampytest.assert_instance(output_emoji_0, Emoji)
        vampytest.assert_eq(output_emoji_0.id, emoji_id_0)
        vampytest.assert_eq(output_emoji_0.name, name_0)
        
        output_emoji_1 = output[1]
        vampytest.assert_instance(output_emoji_1, Emoji)
        vampytest.assert_eq(output_emoji_1.id, emoji_id_1)
        vampytest.assert_eq(output_emoji_1.name, name_1)
        
        vampytest.assert_eq(
            client.application._cache_emojis,
            {
                emoji_id_0: output_emoji_0,
                emoji_id_1: output_emoji_1,
            },
        )
    
    finally:
        client._delete()
        client = None
