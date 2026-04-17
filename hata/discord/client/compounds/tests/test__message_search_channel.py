import vampytest

from ....message import MessageSearchQuery, MessageSearchResponse

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_search_channel__stuffed():
    """
    Tests whether ``Client.message_search_channel`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202601100002
    channel_id = 202601100003
    
    
    mock_api_message_search_channel_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    message_search_query = MessageSearchQuery(
        limit = 10,
    )
    
    message_search_response = MessageSearchResponse(
        result_count = 10,
    )
    
    
    async def mock_api_message_search_channel(input_channel_id, input_query):
        nonlocal mock_api_message_search_channel_called
        nonlocal message_search_query
        nonlocal message_search_response
        
        mock_api_message_search_channel_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(input_query, message_search_query.to_data())
        
        return message_search_response.to_data()
    
    api.message_search_channel = mock_api_message_search_channel
        
    try:
        output = await client.message_search_channel(channel_id, message_search_query)
        vampytest.assert_true(mock_api_message_search_channel_called)
        
        vampytest.assert_instance(output, MessageSearchResponse)
        vampytest.assert_eq(output, message_search_response)
    finally:
        client._delete()
        client = None
