import vampytest

from ....message import MessageSearchQuery, MessageSearchResponse

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_search_guild__stuffed():
    """
    Tests whether ``Client.message_search_guild`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202601100000
    guild_id = 202601100001
    
    
    mock_api_message_search_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    message_search_query = MessageSearchQuery(
        limit = 10,
    )
    
    message_search_response = MessageSearchResponse(
        result_count = 10,
    )
    
    
    async def mock_api_message_search_guild(input_guild_id, input_query):
        nonlocal mock_api_message_search_guild_called
        nonlocal message_search_query
        nonlocal message_search_response
        
        mock_api_message_search_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(input_query, message_search_query.to_data())
        
        return message_search_response.to_data()
    
    api.message_search_guild = mock_api_message_search_guild
        
    try:
        output = await client.message_search_guild(guild_id, message_search_query)
        vampytest.assert_true(mock_api_message_search_guild_called)
        
        vampytest.assert_instance(output, MessageSearchResponse)
        vampytest.assert_eq(output, message_search_response)
    finally:
        client._delete()
        client = None
