__all__ = ()

from ...application_command.application_command.constants import (
    APPLICATION_COMMAND_NAME_LENGTH_MAX, APPLICATION_COMMAND_NAME_LENGTH_MIN
)
from ...field_parsers import entity_id_parser_factory, preinstanced_parser_factory
from ...field_putters import entity_id_putter_factory, preinstanced_putter_factory
from ...field_validators import (
    entity_id_validator_factory, entity_validator_factory, force_string_validator_factory,
    nullable_string_array_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('message_interaction_id')


# name & sub_command_name_stack

def parse_name_and_sub_command_name_stack(data):
    """
    Parses out the message interaction's name and sub command name stack from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Message interaction data.
    
    Returns
    -------
    name : `str`
        Message interaction name.
    sub_command_name_stack : `None`, `tuple` of `str`
        The sub-command-group and sub-command names.
    """
    raw_name = data.get('name', None)
    if raw_name is None:
        name = ''
        sub_command_name_stack = None
    
    else:
        name_split = raw_name.split(' ')
        
        name_split_length = len(name_split)
        if name_split_length == 1:
            name = name_split[0]
            sub_command_name_stack = None
        
        elif name_split_length > 1:
            name = name_split[0]
            sub_command_name_stack = (*name_split[1:],)
        
        else:
            name = ''
            sub_command_name_stack = None
    
    return name, sub_command_name_stack


def put_name_and_sub_command_name_stack_into(name_and_sub_command_name_stack, data, defaults):
    """
    Puts the message interaction's name and sub command name stack into the given `data` json serializable object.
    
    Parameters
    ----------
    name_and_sub_command_name_stack : `tuple` (`str`, `None` | `tuple` of `str`)
       Message interaction name and sub command name stack.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    name, sub_command_name_stack = name_and_sub_command_name_stack
    if sub_command_name_stack is None:
        raw_name = name
    else:
        raw_name = ' '.join([name, *sub_command_name_stack])
    
    data['name'] = raw_name
    return data


validate_name = force_string_validator_factory(
    'name', APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX
)

validate_sub_command_name_stack = nullable_string_array_validator_factory('sub_command_name_stack', ordered = False)

# type

parse_type = preinstanced_parser_factory(
    'type', NotImplemented, NotImplemented, include = 'InteractionType', include_default_attribute_name = 'none'
)

put_type_into = preinstanced_putter_factory('type')

validate_type = preinstanced_validator_factory('type', NotImplemented, include = 'InteractionType')

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
    user_data = data.get('user', None)
    if user_data is None:
        return ZEROUSER
    
    return User.from_data(user_data, data.get('member', None), guild_id)


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
    data['user'] =  user.to_data(defaults = defaults, include_internals = True)
    
    if guild_id:
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            data['member'] = guild_profile.to_data(defaults = defaults, include_internals = True)
    
    return data


validate_user = entity_validator_factory('user', ClientUserBase)
