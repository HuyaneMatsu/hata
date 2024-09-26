__all__ = ()

from ...field_validators import force_date_time_validator_factory
from ...sticker import create_partial_sticker_data
from ...utils import DISCORD_EPOCH_START, datetime_to_timestamp, timestamp_to_datetime

from ..message import MessageFlag, MessageType
from ..message.fields import (
    parse_attachments as _parse_attachments, parse_components as _parse_components, parse_content as _parse_content,
    parse_edited_at as _parse_edited_at, parse_embeds as _parse_embeds, parse_flags as _parse_flags,
    parse_mentioned_role_ids as _parse_mentioned_role_ids, parse_mentioned_users as _parse_mentioned_users,
    parse_stickers as _parse_stickers, parse_type as _parse_type, validate_attachments, validate_components,
    validate_content, validate_edited_at, validate_embeds, validate_flags, validate_mentioned_role_ids,
    validate_mentioned_users, validate_stickers, validate_type
)


# attachments

def parse_attachments(data):
    """
    Parses out attachments value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    attachments : `None | tuple<Attachment>`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_attachments(message_data)


def put_attachments_into(attachments, data, defaults):
    """
    Serializes the given attachments into the given data.
    
    Parameters
    ----------
    attachments : `None | tuple<Attachment>`
        The attachments to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (attachments is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if attachments is None:
            attachment_datas = []
        else:
            attachment_datas = [
                attachment.to_data(defaults = defaults, include_internals = True) for attachment in attachments
            ]
        
        message_data['attachments'] = attachment_datas
    
    return data


# components

def parse_components(data):
    """
    Parses out components value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    components : `None | tuple<Component>`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_components(message_data)


def put_components_into(components, data, defaults):
    """
    Serializes the given components into the given data.
    
    Parameters
    ----------
    components : `None | tuple<Component>`
        The components to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (components is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if components is None:
            component_datas = []
        else:
            component_datas = [component.to_data(defaults = defaults) for component in components]
        
        message_data['components'] = component_datas
    
    return data


# content

def parse_content(data):
    """
    Parses out content value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    content : `None | str`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_content(message_data)


def put_content_into(content, data, defaults):
    """
    Serializes the given content into the given data.
    
    Parameters
    ----------
    content : `None | str`
        The content to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (content is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if content is None:
            content = ''
        
        message_data['content'] = content
    
    return data


# created_at

def parse_created_at(data):
    """
    Parses out created at value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    created_at : `None | DateTime`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return DISCORD_EPOCH_START
    
    created_at = message_data.get('timestamp', None)
    if (created_at is None):
        return DISCORD_EPOCH_START
    
    return timestamp_to_datetime(created_at)


def put_created_at_into(created_at, data, defaults):
    """
    Serializes the given created at value into the given data.
    
    Parameters
    ----------
    created_at : `None | DateTime`
        The created at value to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (created_at != DISCORD_EPOCH_START) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        message_data['timestamp'] = datetime_to_timestamp(created_at)
    
    return data


validate_created_at = force_date_time_validator_factory('created_at')

# edited_at

def parse_edited_at(data):
    """
    Parses out edited at value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    edited_at : `None | DateTime`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_edited_at(message_data)


def put_edited_at_into(edited_at, data, defaults):
    """
    Serializes the given created at value into the given data.
    
    Parameters
    ----------
    edited_at : `None | DateTime`
        The created at value to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (edited_at is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if (edited_at is None):
            timestamp = None
        else:
            timestamp = datetime_to_timestamp(edited_at)
        
        message_data['edited_timestamp'] = timestamp
    
    return data


# embeds

def parse_embeds(data):
    """
    Parses out embeds value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    embeds : `None | tuple<Embed>`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_embeds(message_data)


def put_embeds_into(embeds, data, defaults):
    """
    Serializes the given embeds into the given data.
    
    Parameters
    ----------
    embeds : `None | tuple<Embed>`
        The embeds to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (embeds is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if embeds is None:
            embed_datas = []
        else:
            embed_datas = [embed.to_data(defaults = defaults) for embed in embeds]
        
        message_data['embeds'] = embed_datas
    
    return data


# flags

def parse_flags(data):
    """
    Parses out flags value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    flags : ``MessageFlag``
    """
    message_data = data.get('message', None)
    if message_data is None:
        return MessageFlag(0)
    
    return _parse_flags(message_data)


def put_flags_into(flags, data, defaults):
    """
    Serializes the given flags into the given data.
    
    Parameters
    ----------
    flags : ``MessageFlag``
        The flags to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if flags or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        message_data['flags'] = int(flags)
    
    return data


# mentioned_users

def parse_mentioned_users(data, guild_id = 0):
    """
    Parses out mentioned users value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's id where the message was created at.
    
    Returns
    -------
    message_mentioned_users : `None | tuple<ClientUserBase>`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_mentioned_users(message_data, guild_id)


def put_mentioned_users_into(mentioned_users, data, defaults, *, guild_id = 0):
    """
    Serializes the given mentioned users into the given data.
    
    Parameters
    ----------
    mentioned_users : `None | tuple<ClientUserBase>`
        The mentioned users to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's id where the message was created at.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (mentioned_users is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
    
        user_mention_datas = []
        
        if (mentioned_users is not None):
            for user in mentioned_users:
                user_data = user.to_data(defaults = defaults, include_internals = True)
                
                if guild_id:
                    try:
                        guild_profile = user.guild_profiles[guild_id]
                    except KeyError:
                        pass
                    else:
                        user_data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
                
                user_mention_datas.append(user_data)
        
        message_data['mentions'] = user_mention_datas
    
    return data


# mentioned_role_ids

def parse_mentioned_role_ids(data):
    """
    Parses out mentioned role ids value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    mentioned_role_ids : ``MessageFlag``
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_mentioned_role_ids(message_data)


def put_mentioned_role_ids_into(mentioned_role_ids, data, defaults):
    """
    Serializes the given mentioned_role_ids into the given data.
    
    Parameters
    ----------
    mentioned_role_ids : ``MessageFlag``
        The mentioned_role_ids to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if mentioned_role_ids or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if mentioned_role_ids is None:
            role_id_array = []
        else:
            role_id_array = [str(role_id) for role_id in mentioned_role_ids]
            
        message_data['mention_roles'] = role_id_array
    
    return data


def parse_stickers(data):
    """
    Parses out stickers value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    stickers : `None | tuple<Sticker>`
    """
    message_data = data.get('message', None)
    if message_data is None:
        return None
    
    return _parse_stickers(message_data)


def put_stickers_into(stickers, data, defaults):
    """
    Serializes the given stickers into the given data.
    
    Parameters
    ----------
    stickers : `None | tuple<Sticker>`
        The stickers to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (stickers is not None) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        if stickers is None:
            sticker_datas = []
        else:
            sticker_datas = [create_partial_sticker_data(sticker) for sticker in stickers]
        
        message_data['sticker_items'] = sticker_datas
    
    return data


# type

def parse_type(data):
    """
    Parses out type value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    message_type : ``MessageType``
    """
    message_data = data.get('message', None)
    if message_data is None:
        return MessageType.default
    
    return _parse_type(message_data)


def put_type_into(message_type, data, defaults):
    """
    Serializes the given type into the given data.
    
    Parameters
    ----------
    message_type : ``MessageType``
        The type to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (message_type is not MessageType.default) or defaults:
        message_data = data.get('message', None)
        if message_data is None:
            message_data = {}
            data['message'] = message_data
        
        message_data['type'] = message_type.value
    
    return data
