__all__ = ()

from scarletio import include

from ...field_parsers import functional_parser_factory
from ...field_putters import functional_putter_factory
from ...field_validators import entity_validator_factory
from ...user import ClientUserBase, User, create_partial_user_from_id

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data


Message = include('Message')

# user

def parse_user(data, guild_id = 0):
    """
    Parses out a user from the given reaction create or delete event data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Reaction event data.
    guild_id : `int` = `0`, Optional
        The guild's identifier where the event is from.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    if guild_id:
        try:
            guild_profile_data = data['member']
        except KeyError:
            pass
        else:
            user_data = guild_profile_data['user']
            return User.from_data(user_data, guild_profile_data, int(guild_id))
    
    return create_partial_user_from_id(int(data['user_id']))


def put_user_into(user, data, defaults, *, guild_id = 0):
    """
    Puts the given user's representation into the given reaction event data.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to serialize.
    data : `dict` of (`str`, `object`) items
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's identifier where the event is from.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['user_id'] = str(user.id)
    
    if guild_id:
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            guild_profile_data = guild_profile.to_data(defaults = defaults, include_internals = True)
            guild_profile_data['user'] = user.to_data(defaults = defaults, include_internals = True)
            
            data['member'] = guild_profile_data
    
    return data


validate_user = entity_validator_factory('user', ClientUserBase)

# emoji

parse_emoji = functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji_into = functional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = entity_validator_factory('emoji', Emoji)

# message

def parse_message(data):
    """
    Parses out a message from the given reaction create or delete event data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Reaction event data.
    
    Returns
    -------
    message : ``Message``
    """
    return Message._create_from_partial_data(data)


def put_message_into(message, data, defaults):
    """
    Puts the given message's representation into the given reaction event data.
    
    Parameters
    ----------
    message : ``Message``
        The message to serialize.
    data : `dict` of (`str`, `object`) items
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['message_id'] = str(message.id)
    data['channel_id'] = str(message.channel_id)
    
    guild_id = message.guild_id
    if defaults or guild_id:
        if guild_id:
            guild_id = str(guild_id)
        else:
            guild_id = None
        
        data['guild_id'] = guild_id
    
    return data

validate_message = entity_validator_factory('message', NotImplemented, include = 'Message')
