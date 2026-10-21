__all__ = (
    'GuildJoinRequest', 'guild_join_request_convert_to_data', 'guild_join_request_create',
    'guild_join_request_create_from_data'
)

from scarletio import RichType

from .fields import (
    parse_actioned_at, parse_actioned_by, parse_created_at, parse_form_field_responses, parse_guild_id, parse_id,
    parse_last_seen_at, parse_rejection_reason, parse_status, parse_user, put_actioned_at, put_actioned_by,
    put_created_at, put_form_field_responses, put_guild_id, put_id, put_last_seen_at, put_rejection_reason,
    put_status, put_user, put_user_id, validate_actioned_at, validate_actioned_by, validate_created_at,
    validate_form_field_responses, validate_guild_id, validate_id, validate_last_seen_at,
    validate_rejection_reason, validate_status, validate_user, validate_user_id, parse_user_id
)
from .preinstanced import GuildJoinRequestStatus


class GuildJoinRequest(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Guild join request received within both `GUILD_JOIN_REQUEST_CREATE` and `GUILD_JOIN_REQUEST_UPDATE` events.
    
    Attributes
    ----------
    actioned_by : ``None | ClientUserBase``
        The user who action the join request.
    
    actioned_at : `None | DateTime`
        When the join request was actioned at.
    
    created_at : `None | DateTime`
        When the join request was created.
    
    form_field_responses : ``None | tuple<GuildJoinRequestFormFieldResponse>``
        The responses the user submitted.
    
    guild_id : `int`
        The respective guild's identifier.
    
    id : `int`
        The guild join request's identifier.
    
    last_seen_at : `None | DateTime`
        When the user was last seen.
    
    rejection_reason : `None | str`
        The reason why the join request was rejected.
    
    status : ``GuildJoinRequestStatus``
        The join request's status.
    
    user : ``None | ClientUserBase``
        The user in context.
    
    user_id : `int`
        The joining user's identifier.
    """
    __slots__ = (
        'actioned_by', 'actioned_at', 'created_at', 'form_field_responses', 'guild_id', 'id', 'last_seen_at',
        'rejection_reason', 'status', 'user', 'user_id',
    )


def guild_join_request_create(
    *,
    actioned_by = ...,
    actioned_at = ...,
    created_at = ...,
    form_field_responses = ...,
    guild_id = ...,
    guild_join_request_id = ...,
    last_seen_at = ...,
    rejection_reason = ...,
    status = ...,
    user = ...,
    user_id = ...,
):
    """
    Creates a new guild join request.
    
    Parameters
    ----------
    actioned_by : ``None | ClientUserBase``, Optional (Keyword only)
        The user who action the join request.
    
    actioned_at : `None | DateTime`, Optional (Keyword only)
        When the join request was actioned at.
    
    created_at : `None | DateTime`, Optional (Keyword only)
        When the join request was created.
    
    form_field_responses : ``None | iterable<GuildJoinRequestFormFieldResponse>``, Optional (Keyword only)
        The responses the user submitted.
    
    guild_id : `int`, Optional (Keyword only)
        The respective guild's identifier.
    
    guild_join_request_id : `int`, Optional (Keyword only)
        The guild join request's identifier.
    
    last_seen_at : `None | DateTime`, Optional (Keyword only)
        When the user was last seen.
    
    rejection_reason : `None | str`, Optional (Keyword only)
        The reason why the join request was rejected.
    
    status : ``GuildJoinRequestStatus``, Optional (Keyword only)
        The join request's status.
    
    user : ``ClientUserBase``, Optional (Keyword only)
        The user in context.
    
    Raises
    ------
    TypeError
        - If a parameter's type is invalid.
    ValueError
        - If a parameter's value is invalid.
    
    Returns
    -------
    guild_join_request : ``GuildJoinRequest``
    """
    # actioned_by
    if actioned_by is ...:
        actioned_by = None
    else:
        actioned_by = validate_actioned_by(actioned_by)
    
    # actioned_at
    if actioned_at is ...:
        actioned_at = None
    else:
        actioned_at = validate_actioned_at(actioned_at)
    
    # created_at
    if created_at is ...:
        created_at = None
    else:
        created_at = validate_created_at(created_at)
    
    # form_field_responses
    if form_field_responses is ...:
        form_field_responses = None
    else:
        form_field_responses = validate_form_field_responses(form_field_responses)
    
    # guild_id
    if guild_id is ...:
        guild_id = 0
    else:
        guild_id = validate_guild_id(guild_id)
    
    # guild_join_request_id
    if guild_join_request_id is ...:
        guild_join_request_id = 0
    else:
        guild_join_request_id = validate_id(guild_join_request_id)
    
    # last_seen_at
    if last_seen_at is ...:
        last_seen_at = None
    else:
        last_seen_at = validate_last_seen_at(last_seen_at)
    
    # rejection_reason
    if rejection_reason is ...:
        rejection_reason = None
    else:
        rejection_reason = validate_rejection_reason(rejection_reason)
    
    # status
    if status is ...:
        status = GuildJoinRequestStatus.started
    else:
        status = validate_status(status)
    
    # user
    if user is ...:
        user = None
    else:
        user = validate_user(user)
    
    # user_id
    if user_id is ...:
        user_id = 0
    else:
        user_id = validate_user_id(user_id)
    
    if (not user_id) and (user is not None):
        user_id = user.id
    
    # Construct
    guild_join_request = object.__new__(GuildJoinRequest)
    guild_join_request.actioned_by = actioned_by
    guild_join_request.actioned_at = actioned_at
    guild_join_request.created_at = created_at
    guild_join_request.form_field_responses = form_field_responses
    guild_join_request.guild_id = guild_id
    guild_join_request.id = guild_join_request_id
    guild_join_request.last_seen_at = last_seen_at
    guild_join_request.rejection_reason = rejection_reason
    guild_join_request.status = status
    guild_join_request.user = user
    guild_join_request.user_id = user_id
    return guild_join_request


def guild_join_request_create_from_data(data):
    """
    Creates a new guild join request from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Received data.
    
    Returns
    -------
    guild_join_request : ``GuildJoinRequest``
    """
    guild_join_request = object.__new__(GuildJoinRequest)
    guild_join_request.actioned_by = parse_actioned_by(data)
    guild_join_request.actioned_at = parse_actioned_at(data)
    guild_join_request.created_at = parse_created_at(data)
    guild_join_request.form_field_responses = parse_form_field_responses(data)
    guild_join_request.guild_id = parse_guild_id(data)
    guild_join_request.id = parse_id(data)
    guild_join_request.last_seen_at = parse_last_seen_at(data)
    guild_join_request.rejection_reason = parse_rejection_reason(data)
    guild_join_request.status = parse_status(data)
    guild_join_request.user = parse_user(data)
    guild_join_request.user_id = parse_user_id(data)
    return guild_join_request


def guild_join_request_convert_to_data(guild_join_request, *, defaults = False):
    """
    Serializes the guild join request.
    
    Parameters
    ----------
    guild_join_request : ``GuildJoinRequest``
        Guild join request to serialise.
    
    defaults : `bool` = `False`, Optional (Keyword only)
        Whether fields of their default value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_actioned_by(guild_join_request.actioned_by, data, defaults)
    put_actioned_at(guild_join_request.actioned_at, data, defaults)
    put_created_at(guild_join_request.created_at, data, defaults)
    put_form_field_responses(guild_join_request.form_field_responses, data, defaults)
    put_guild_id(guild_join_request.guild_id, data, defaults)
    put_id(guild_join_request.id, data, defaults)
    put_last_seen_at(guild_join_request.last_seen_at, data, defaults)
    put_rejection_reason(guild_join_request.rejection_reason, data, defaults)
    put_status(guild_join_request.status, data, defaults)
    put_user(guild_join_request.user, data, defaults)
    put_user_id(guild_join_request.user_id, data, defaults)
    return data

