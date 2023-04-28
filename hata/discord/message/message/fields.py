__all__ = ()

from ...field_parsers import nullable_entity_parser_factory, entity_id_parser_factory, preinstanced_parser_factory
from ...field_putters import nullable_entity_optional_putter_factory, entity_id_putter_factory, \
    preinstanced_putter_factory
from ...field_validators import nullable_entity_validator_factory, entity_id_validator_factory, \
    preinstanced_validator_factory, default_entity_validator

from ..message_role_subscription import MessageRoleSubscription
from .preinstanced import MessageType
from ...user import User, ZEROUSER, UserBase
from ...webhook import WebhookRepr, WebhookType, create_partial_webhook_from_id, WebhookBase

# author

def parse_author(data, channel_id = 0, guild_id = 0):
    """
    Parses the message's author from its data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    channel_id : `int` = `0`, Optional
        The channel's id where the message was created at.
    guild_id : `int` = `0`, Optional
        The guild's id where the message was created at.
    
    Returns
    -------
    author : ``UserBase``
    """
    author_data = data.get('author', None)
    
    webhook_id = data.get('webhook_id', None)
    if (webhook_id is not None):
        application_id = data.get('application_id', None)
        if ((application_id is None) or (webhook_id != application_id)):
            if data.get('message_reference', None) is None:
                webhook_type = WebhookType.bot
            else:
                webhook_type = WebhookType.server
            
            webhook_id = int(webhook_id)
            if author_data is None:
                return create_partial_webhook_from_id(webhook_id, '', webhook_type = webhook_type)
            
            return WebhookRepr.from_data(author_data, webhook_id, webhook_type, channel_id)
    
    if author_data is None:
        return ZEROUSER
    
    return User.from_data(author_data, data.get('member', None), guild_id)


def put_author_into(author, data, defaults, * guild_id):
    """
    Puts the message author's data into the given `data` json serializable object.
    
    Parameters
    ----------
    author : ``UserBase``
        Message author.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's id where the message was created at.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['user'] =  author.to_data(defaults = defaults, include_internals = True)
    
    if guild_id:
        try:
            guild_profile = author.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
    
    # If the message as created by a webhook, put its into the data too.
    if isinstance(author, WebhookBase):
        data['webhook_id'] = str(author.id)
    elif defaults:
        data['webhook_id'] = None
    
    return data


validate_author = default_entity_validator('author', UserBase, default = ZEROUSER)

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', NotImplemented, include = 'Channel')

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('message_id')

# message_id

def parse_message_id(data):
    """
    Parses out a message id from the given data. Not like `parse_id` it first checks for `message_id`
    and then for `id` keys.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message data.
    
    Returns
    -------
    message_id : `int`
    """
    try:
        message_id = data['message_id']
    except KeyError:
        pass
    else:
        if message_id is None:
            return 0
        
        return int(message_id)
    
    try:
        message_id = data['id']
    except KeyError:
        pass
    else:
        if message_id is None:
            return 0
        
        return int(message_id)
    
    return 0

put_message_id_into = entity_id_putter_factory('message_id')

# role_subscription

parse_role_subscription = nullable_entity_parser_factory('role_subscription_data', MessageRoleSubscription)
put_role_subscription_into = nullable_entity_optional_putter_factory(
    'role_subscription_data', MessageRoleSubscription
)
validate_role_subscription = nullable_entity_validator_factory('role_subscription', MessageRoleSubscription)

# type

parse_type = preinstanced_parser_factory('type', MessageType, MessageType.default)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', MessageType)
