__all__ = (
    'GuildJoinRequestDeleteEvent', 'guild_join_request_event_convert_to_data', 'guild_join_request_delete_event_create',
    'guild_join_request_delete_event_create_from_data'
)

from scarletio import RichType

from .fields import (
    parse_guild_id, parse_guild_join_request_id, parse_user_id, put_guild_id, put_guild_join_request_id, put_user_id,
    validate_guild_id, validate_guild_join_request_id, validate_user_id
)


class GuildJoinRequestDeleteEvent(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Represents a `GUILD_JOIN_REQUEST_DELETE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event is for.
    
    guild_join_request_id : `int`
        The guild join request's identifier.
    
    user_id : `int`
        The user's identifier whos join request was deleted.
    """
    __slots__ = ('guild_id', 'guild_join_request_id', 'user_id')


def guild_join_request_delete_event_create(*, guild_id = ..., guild_join_request_id = ..., user_id = ...):
    """
    Creates a new guild join request delete event.
    
    Parameters
    ----------
    guild_id : `int`, Optional (Keyword only)
        The guild's identifier where the event will be.
    
    guild_join_request_id : `int`, Optional (Keyword only)
        The guild join request's identifier.
    
    user_id : `int`, Optional (Keyword only)
        The user's identifier whos join request was deleted.
    
    Raises
    ------
    TypeError
        - If a parameter's type is invalid.
    ValueError
        - If a parameter's value is invalid.
    """
    # guild_id
    if guild_id is ...:
        guild_id = 0
    else:
        guild_id = validate_guild_id(guild_id)
    
    if guild_join_request_id is ...:
        guild_join_request_id = 0
    else:
        guild_join_request_id = validate_guild_join_request_id(guild_join_request_id)
    
    # user_id
    if user_id is ...:
        user_id = 0
    else:
        user_id = validate_user_id(user_id)
    
    # Construct
    guild_join_request_delete_event = object.__new__(GuildJoinRequestDeleteEvent)
    guild_join_request_delete_event.guild_id = guild_id
    guild_join_request_delete_event.guild_join_request_id = guild_join_request_id
    guild_join_request_delete_event.user_id = user_id
    return guild_join_request_delete_event

    
def guild_join_request_delete_event_create_from_data(data):
    """
    Creates a new guild join request delete event from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild join request delete event data.
    
    Returns
    -------
    guild_join_request_delete_event : `GuildJoinRequestDeleteEvent`
    """
    guild_join_request_delete_event = object.__new__(GuildJoinRequestDeleteEvent)
    guild_join_request_delete_event.guild_id = parse_guild_id(data)
    guild_join_request_delete_event.guild_join_request_id = parse_guild_join_request_id(data)
    guild_join_request_delete_event.user_id = parse_user_id(data)
    return guild_join_request_delete_event


def guild_join_request_event_convert_to_data(guild_join_request_delete_event, *, defaults = False):
    """
    Serializes the guild join request delete event.
    
    Parameters
    ----------
    guild_join_request_delete_event : ``GuildJoinRequestDeleteEvent``
        The guild join request event to serialise.
    
    defaults : `bool` = `False`, Optional (Keyword only)
        Whether fields of their default value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_guild_id(guild_join_request_delete_event.guild_id, data, defaults)
    put_guild_join_request_id(guild_join_request_delete_event.guild_join_request_id, data, defaults)
    put_user_id(guild_join_request_delete_event.user_id, data, defaults)
    return data
