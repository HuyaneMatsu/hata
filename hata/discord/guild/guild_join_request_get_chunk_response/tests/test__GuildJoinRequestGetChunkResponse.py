import vampytest

from ...guild_join_request import (
    guild_join_request_create, guild_join_request_convert_to_data
)

from ..guild_join_request_get_chunk_response import (
    GuildJoinRequestGetChunkResponse, guild_join_request_get_chunk_response_convert_to_data,
    guild_join_request_get_chunk_response_create,  guild_join_request_get_chunk_response_create_from_data
)


def assert_guild_join_request_get_chunk_response_fields_set(response):
    vampytest.assert_instance(response, GuildJoinRequestGetChunkResponse)
    vampytest.assert_instance(response.guild_join_requests, tuple, nullable = True)
    vampytest.assert_instance(response.total, int)


def test__guild_join_request_get_chunk_response_create__no_fields():
    response = guild_join_request_get_chunk_response_create()
    assert_guild_join_request_get_chunk_response_fields_set(response)


def test__guild_join_request_get_chunk_response_create__all_fields():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180006),
        guild_join_request_create(guild_join_request_id = 202610180007),
    )
    total = 2
    
    response = guild_join_request_get_chunk_response_create(
        guild_join_requests = guild_join_requests,
        total = total,
    )
    assert_guild_join_request_get_chunk_response_fields_set(response)
    vampytest.assert_eq(response.guild_join_requests, guild_join_requests)
    vampytest.assert_eq(response.total, total)


def test__guild_join_request_get_chunk_response_create_from_data():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180008),
        guild_join_request_create(guild_join_request_id = 202610180009),
    )
    total = 2
    
    data = {
        'guild_join_requests': [
            guild_join_request_convert_to_data(request)
            for request in guild_join_requests
        ],
        'total': total,
    }
    
    response = guild_join_request_get_chunk_response_create_from_data(data)
    vampytest.assert_eq(response.guild_join_requests, guild_join_requests)
    vampytest.assert_eq(response.total, total)


def test__guild_join_request_get_chunk_response_convert_to_data():
    guild_join_requests = (
        guild_join_request_create(guild_join_request_id = 202610180010),
        guild_join_request_create(guild_join_request_id = 202610180011),
    )
    total = 2
    
    response = guild_join_request_get_chunk_response_create(
        guild_join_requests = guild_join_requests,
        total = total,
    )
    
    vampytest.assert_eq(
        guild_join_request_get_chunk_response_convert_to_data(response, defaults = True),
        {
            'guild_join_requests': [
                guild_join_request_convert_to_data(request, defaults = True)
                for request in guild_join_requests
            ],
            'total': total,
        },
    )
