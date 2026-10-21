from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....guild import (
    GuildJoinRequestStatus, guild_join_request_create, guild_join_request_get_chunk_response_convert_to_data,
    guild_join_request_get_chunk_response_create
)
from ....utils import datetime_to_id

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_join_request_get_chunk():
    client_id = 202610200010
    guild_id = 202610200011
    guild_join_request_id_0 = 202610200012
    guild_join_request_id_1 = 202610200013
    status = GuildJoinRequestStatus.rejected
    
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    before = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    limit = 49
    
    mock_api_guild_join_request_get_chunk_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    expected_output = guild_join_request_get_chunk_response_create(
        guild_join_requests = (
            guild_join_request_create(guild_join_request_id = guild_join_request_id_0),
            guild_join_request_create(guild_join_request_id = guild_join_request_id_1),
        ),
        total = 2,
    )
    
    async def mock_api_guild_join_request_get_chunk(input_guild_id, query):
        nonlocal mock_api_guild_join_request_get_chunk_called
        nonlocal guild_id
        nonlocal status
        nonlocal before
        nonlocal after
        nonlocal limit
        nonlocal expected_output
        
        mock_api_guild_join_request_get_chunk_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(
            query,
            {
                'after': datetime_to_id(after),
                'before': datetime_to_id(before),
                'limit': limit,
                'status': status.value,
            },
        )
        return guild_join_request_get_chunk_response_convert_to_data(expected_output)
    
    api.guild_join_request_get_chunk = mock_api_guild_join_request_get_chunk
    
    try:
        output = await client.guild_join_request_get_chunk(
            guild_id,
            after = after,
            before = before,
            limit = limit,
            status = status,
        )
        vampytest.assert_true(mock_api_guild_join_request_get_chunk_called)
        
        vampytest.assert_eq(output, expected_output)
    finally:
        client._delete()
        client = None
