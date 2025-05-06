__all__ = ()

from scarletio import include

from ...field_validators import entity_validator_factory
from ...user import ClientUserBase, ZEROUSER, create_partial_user_from_id
from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_putter_factory
from ...field_validators import entity_id_validator_factory


# answer_id

parse_answer_id = entity_id_parser_factory('answer_id')
put_answer_id = entity_id_putter_factory('answer_id')
validate_answer_id = entity_id_validator_factory('answer_id')

Message = include('Message')

# message

def parse_message(data):
    """
    Parses out a message from the given vote add or delete event data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Vote event data.
    
    Returns
    -------
    message : ``Message``
    """
    return Message._create_from_partial_data(data)


def put_message(message, data, defaults):
    """
    Puts the given message's representation into the given vote event data.
    
    Parameters
    ----------
    message : ``Message``
        The message to serialize.
    data : `dict<str, object>`
        Vote event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
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

# user


def parse_user(data):
    """
    Parses out the vote event's users.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Vote data.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    user_id = data.get('user_id', None)
    if user_id is None:
        return ZEROUSER
    
    return create_partial_user_from_id(int(user_id))

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
