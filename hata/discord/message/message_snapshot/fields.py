__all__ = ()

from ...field_validators import force_date_time_validator_factory
from ...utils import DISCORD_EPOCH_START, datetime_to_timestamp, timestamp_to_datetime

from ..message import MessageFlag
from ..message.fields import (
    parse_attachments as _parse_attachments, parse_content as _parse_content, parse_edited_at as _parse_edited_at,
    parse_embeds as _parse_embeds, parse_flags as _parse_flags, validate_attachments, validate_content,
    validate_edited_at, validate_embeds, validate_flags
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
