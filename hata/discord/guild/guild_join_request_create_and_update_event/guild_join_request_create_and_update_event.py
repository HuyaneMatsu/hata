__all__ = (
    'GuildJoinRequestCreateAndUpdateEvent', 'guild_join_request_create_and_update_event_convert_to_data',
    'guild_join_request_create_and_update_event_create', 'guild_join_request_create_and_update_event_create_from_data'
)

from scarletio import RichType

from ..guild_join_request import GuildJoinRequestStatus

from .fields import (
    parse_guild_id, parse_guild_join_request, parse_status, put_guild_id, put_guild_join_request, put_status,
    validate_guild_id, validate_guild_join_request, validate_status
)


class GuildJoinRequestCreateAndUpdateEvent(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents a `GUILD_JOIN_REQUEST_CREATE` and an `GUILD_JOIN_REQUEST_UPDATE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event is for.
    
    guild_join_request : ``None | GuildJoinRequest``
        The guild join request.
    
    status : ``GuildJoinRequestStatus``
        The user's identifier whos join request was updated.
    """
    __slots__ = ('guild_id', 'guild_join_request', 'status')


def guild_join_request_create_and_update_event_create(*, guild_id = ..., guild_join_request = ..., status = ...):
    """
    Creates a new guild join request create and update event.
    
    Parameters
    ----------
    guild_id : `int`, Optional (Keyword only)
        The guild's identifier where the event will be.
    
    guild_join_request : ``None | GuildJoinRequest``, Optional (Keyword only)
        The guild join request.
    
    status : ``None | str | GuildJoinRequestStatus``, Optional (Keyword only)
        The guild join request's status.
    
    Raises
    ------
    TypeError
        - If a parameter's type is invalid.
    ValueError
        - If a parameter's value is invalid.
    
    Returns
    -------
    guild_join_request_create_and_update_event : ``GuildJoinRequestCreateAndUpdateEvent``
    """
    # guild_id
    if guild_id is ...:
        guild_id = 0
    else:
        guild_id = validate_guild_id(guild_id)
    
    if guild_join_request is ...:
        guild_join_request = None
    else:
        guild_join_request = validate_guild_join_request(guild_join_request)
    
    # status
    if status is ...:
        status = GuildJoinRequestStatus.started
    else:
        status = validate_status(status)
    
    # Construct
    guild_join_request_create_and_update_event = object.__new__(GuildJoinRequestCreateAndUpdateEvent)
    guild_join_request_create_and_update_event.guild_id = guild_id
    guild_join_request_create_and_update_event.guild_join_request = guild_join_request
    guild_join_request_create_and_update_event.status = status
    return guild_join_request_create_and_update_event


def guild_join_request_create_and_update_event_create_from_data(data):
    """
    Creates a new guild join request create or update event from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild join request update event data.
    
    Returns
    -------
    guild_join_request_create_and_update_event : ``GuildJoinRequestCreateAndUpdateEvent``
    """
    guild_join_request_create_and_update_event = object.__new__(GuildJoinRequestCreateAndUpdateEvent)
    guild_join_request_create_and_update_event.guild_id = parse_guild_id(data)
    guild_join_request_create_and_update_event.guild_join_request = parse_guild_join_request(data)
    guild_join_request_create_and_update_event.status = parse_status(data)
    return guild_join_request_create_and_update_event


def guild_join_request_create_and_update_event_convert_to_data(
    guild_join_request_create_and_update_event, *, defaults = False
):
    """
    Serializes the guild join request create or update event.
    
    Parameters
    ----------
    guild_join_request_create_and_update_event : ``GuildJoinRequestCreateAndUpdateEvent``
        Instance to serialise.
    
    defaults : `bool` = `False`, Optional (Keyword only)
        Whether fields of their default value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_guild_id(guild_join_request_create_and_update_event.guild_id, data, defaults)
    put_guild_join_request(guild_join_request_create_and_update_event.guild_join_request, data, defaults)
    put_status(guild_join_request_create_and_update_event.status, data, defaults)
    return data
