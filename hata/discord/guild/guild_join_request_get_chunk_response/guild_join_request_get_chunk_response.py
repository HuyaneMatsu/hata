__all__ = (
    'GuildJoinRequestGetChunkResponse', 'guild_join_request_get_chunk_response_convert_to_data',
    'guild_join_request_get_chunk_response_create', 'guild_join_request_get_chunk_response_create_from_data'
)

from scarletio import RichType

from .fields import (
    parse_guild_join_requests, parse_total, put_guild_join_requests, put_total, validate_guild_join_requests,
    validate_total
)


class GuildJoinRequestGetChunkResponse(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Response of a guild join requests get chunk request.
    
    Attributes
    ----------
    guild_join_requests : ``None | tuple<GuildJoinRequest>``
        The guild join requests received as part of the chunk.
    
    total : `int`
        The total amount of users.
    """
    __slots__ = ('guild_join_requests', 'total')


def guild_join_request_get_chunk_response_create(*, guild_join_requests = ..., total = ...):
    """
    Creates a new instance.
    
    Parameters
    ----------
    guild_join_requests : ``None | iterable<GuildJoinRequest>``, Optional (Keyword only)
        The guild join requests received as part of the chunk.
    
    total : `int`, Optional (Keyword only)
        The total amount of users.
    
    Raises
    ------
    TypeError
        - If a parameter's value is incorrect.
    ValueError
        - if a parameter's value is incorrect.
    """
    # guild_join_requests
    if guild_join_requests is ...:
        guild_join_requests = None
    else:
        guild_join_requests = validate_guild_join_requests(guild_join_requests)
    
    if total is ...:
        total = (0 if guild_join_requests is None else len(guild_join_requests))
    else:
        total = validate_total(total)
    
    response = object.__new__(GuildJoinRequestGetChunkResponse)
    response.guild_join_requests = guild_join_requests
    response.total = total
    return response


def guild_join_request_get_chunk_response_create_from_data(data):
    """
    Creates an instance from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to create instance from.
    
    Returns
    -------
    response : ``GuildJoinRequestGetChunkResponse``
    """
    response = object.__new__(GuildJoinRequestGetChunkResponse)
    response.guild_join_requests = parse_guild_join_requests(data)
    response.total = parse_total(data)
    return response


def guild_join_request_get_chunk_response_convert_to_data(response, *, defaults = False):
    """
    Converts the response to data.
    
    Parameters
    ----------
    response : ``GuildJoinRequestGetChunkResponse``
        Response to convert.
    
    defaults : `bool` = `False`, Optional (Keyword only)
        Whether values ast heir defaults should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_guild_join_requests(response.guild_join_requests, data, defaults)
    put_total(response.total, data, defaults)
    return data
