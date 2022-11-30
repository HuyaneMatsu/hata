__all__ = ()

from ...channel import Channel, create_partial_channel_from_data
from ...field_validators import nullable_entity_dictionary_validator_factory
from ...message import Attachment, Message
from ...role import Role
from ...user import ClientUserBase, User

# attachments

def parse_attachments(data):
    """
    Parsers out the resolved attachments from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Resolved data.
    
    Returns
    -------
    attachments : `None`, `dict` of (`int`, ``Attachment``) items
    """
    resolved_attachment_datas = data.get('attachments', None)
    if (resolved_attachment_datas is None) or (not resolved_attachment_datas):
        return
    
    resolved_attachments = {}
    
    for attachment_data in resolved_attachment_datas.values():
        attachment = Attachment.from_data(attachment_data)
        resolved_attachments[attachment.id] = attachment
    
    return resolved_attachments


def put_attachments_into(attachments, data, defaults):
    """
    Puts the given `attachments` into the given `data` json serializable object.
    
    Parameters
    ----------
    attachments : `None`, `dict` of (`int`, ``Attachment``) items
        Resolved attachments.
    
    data : `dict` of (`str`, `Any`) items
        Interaction resolved data.
    
    defaults : `bool`
        Whether default fields values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (attachments is not None):
        resolved_attachment_datas = {}
        
        if (attachments is not None):
            for attachment in attachments.values():
                resolved_attachment_datas[str(attachment.id)] = attachment.to_data(
                    defaults = defaults, include_internals = True
                )
        
        data['attachments'] = resolved_attachment_datas
    
    return data


validate_attachments = nullable_entity_dictionary_validator_factory('attachments', Attachment)

# channels

def parse_channels(data, interaction_event):
    """
    Parsers out the resolved channels from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Resolved data.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    channels : `None`, `dict` of (`int`, ``Channel``) items
    """
    resolved_channel_datas = data.get('channels', None)
    if (resolved_channel_datas is None) or (not resolved_channel_datas):
        return
    
    resolved_channels = {}
    
    for channel_data in resolved_channel_datas.values():
        channel = create_partial_channel_from_data(channel_data, interaction_event.guild_id)
        if (channel is not None):
            resolved_channels[channel.id] = channel
    
    return resolved_channels


def put_channels_into(channels, data, defaults):
    """
    Puts the given `channels` into the given `data` json serializable object.
    
    Parameters
    ----------
    channels : `None`, `dict` of (`int`, ``Channel``) items
        Resolved channels.
    
    data : `dict` of (`str`, `Any`) items
        Interaction resolved data.
    
    defaults : `bool`
        Whether default fields values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (channels is not None):
        resolved_channel_datas = {}
        
        if (channels is not None):
            for channel in channels.values():
                resolved_channel_datas[str(channel.id)] = channel.to_data(
                    defaults = defaults, include_internals = True
                )
        
        data['channels'] = resolved_channel_datas
    
    return data


validate_channels = nullable_entity_dictionary_validator_factory('channels', Channel)

# roles

def parse_roles(data, interaction_event):
    """
    Parsers out the resolved roles from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Resolved data.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    roles : `None`, `dict` of (`int`, ``Role``) items
    """
    resolved_role_datas = data.get('roles', None)
    if (resolved_role_datas is None) or (not resolved_role_datas):
        return
    
    resolved_roles = {}
    
    for role_data in resolved_role_datas.values():
        role = Role.from_data(role_data, interaction_event.guild_id)
        resolved_roles[role.id] = role
    
    return resolved_roles


def put_roles_into(roles, data, defaults):
    """
    Puts the given `roles` into the given `data` json serializable object.
    
    Parameters
    ----------
    roles : `None`, `dict` of (`int`, ``Role``) items
        Resolved roles.
    
    data : `dict` of (`str`, `Any`) items
        Interaction resolved data.
    
    defaults : `bool`
        Whether default fields values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (roles is not None):
        resolved_role_datas = {}
        
        if (roles is not None):
            for role in roles.values():
                resolved_role_datas[str(role.id)] = role.to_data(
                    defaults = defaults, include_internals = True
                )
        
        data['roles'] = resolved_role_datas
    
    return data


validate_roles = nullable_entity_dictionary_validator_factory('roles', Role)

# messages

def parse_messages(data):
    """
    Parsers out the resolved messages from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Resolved data.
    
    Returns
    -------
    messages : `None`, `dict` of (`int`, ``Message``) items
    """
    resolved_message_datas = data.get('messages', None)
    if (resolved_message_datas is None) or (not resolved_message_datas):
        return
    
    resolved_messages = {}
    
    for message_data in resolved_message_datas.values():
        message = Message.from_data(message_data)
        resolved_messages[message.id] = message
    
    return resolved_messages


def put_messages_into(messages, data, defaults):
    """
    Puts the given `messages` into the given `data` json serializable object.
    
    Parameters
    ----------
    messages : `None`, `dict` of (`int`, ``Message``) items
        Resolved messages.
    
    data : `dict` of (`str`, `Any`) items
        Interaction resolved data.
    
    defaults : `bool`
        Whether default fields values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (messages is not None):
        resolved_message_datas = {}
        
        if (messages is not None):
            for message in messages.values():
                resolved_message_datas[str(message.id)] = message.to_data(
                    defaults = defaults, include_internals = True
                )
        
        data['messages'] = resolved_message_datas
    
    return data


validate_messages = nullable_entity_dictionary_validator_factory('messages', Message)

# users

def parse_users(data, interaction_event):
    """
    Parsers out the resolved users from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Resolved data.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    messages : `None`, `dict` of (`int`, ``Message``) items
    """
    resolved_user_datas = data.get('users', None)
    if (resolved_user_datas is None) or (not resolved_user_datas):
        return
    
    resolved_guild_profile_datas = data.get('members', None)

    resolved_users = {}
    
    for user_id, user_data in resolved_user_datas.items():
        
        if resolved_guild_profile_datas is None:
            guild_profile_data = None
        else:
            guild_profile_data = resolved_guild_profile_datas.get(user_id, None)
        
        user = User.from_data(user_data, guild_profile_data, interaction_event.guild_id)
        resolved_users[user.id] = user
        
        if (guild_profile_data is not None):
            interaction_event._add_cached_user(user)

    return resolved_users


def put_users_into(users, data, defaults, *, interaction_event = None):
    """
    Puts the given `users` into the given `data` json serializable object.
    
    Parameters
    ----------
    users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        Resolved users.
    
    data : `dict` of (`str`, `Any`) items
        Interaction resolved data.
    
    defaults : `bool`
        Whether default fields values should be included as well.
    
    interaction_event : ``InteractionEvent`` = `None`, Optional (Keyword only)
        The respective guild's identifier to use for handing user guild profiles.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (users is not None):
        resolved_user_datas = {}
        resolved_guild_profile_datas = {}
        
        if (users is not None):
            if interaction_event is None:
                guild_id = 0
            else:
                guild_id = interaction_event.guild_id
            
            for user in users.values():
                resolved_user_datas[str(user.id)] = user.to_data(
                    defaults = defaults, include_internals = True
                )
                
                guild_profile = user.guild_profiles.get(guild_id, None)
                if (guild_profile is not None):
                    resolved_guild_profile_datas[str(user.id)] = guild_profile.to_data(
                        defaults = defaults, include_internals = True
                    )
        
        data['users'] = resolved_user_datas
        data['members'] = resolved_guild_profile_datas
    
    return data


validate_users = nullable_entity_dictionary_validator_factory('users', ClientUserBase)
