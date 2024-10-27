__all__ = ()

from ...application import ApplicationIntegrationType
from ...application_command.application_command.constants import (
    NAME_LENGTH_MAX as APPLICATION_COMMAND_NAME_LENGTH_MAX, NAME_LENGTH_MIN as APPLICATION_COMMAND_NAME_LENGTH_MIN
)
from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, nullable_entity_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    default_entity_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    nullable_entity_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    default_entity_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory, nullable_string_array_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

# authorizer_user_ids

def parse_authorizer_user_ids(data):
    """
    Parses authorizer user identifiers.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    authorizer_user_ids : `None | dict<ApplicationIntegrationType, int>`
    """
    authorizer_user_ids_data = data.get('authorizing_integration_owners', None)
    if (authorizer_user_ids_data is None) or (not authorizer_user_ids_data):
        return None
    
    authorizer_user_ids = {}
    
    for key, value in authorizer_user_ids_data.items():
        integration_type = ApplicationIntegrationType.get(ApplicationIntegrationType.VALUE_TYPE(key))
        user_id = int(value)
        authorizer_user_ids[integration_type] = user_id
    
    return authorizer_user_ids


def put_authorizer_user_ids_into(authorizer_user_ids, data, defaults):
    """
    Serializes the authorizer user identifiers.
    
    Parameters
    ----------
    authorizer_user_ids : `None | dict<ApplicationIntegrationType, int>`
        The identifiers of the authorizer users.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    authorizer_user_ids_data = {}
    
    if (authorizer_user_ids is not None):
        for integration_type, user_id in authorizer_user_ids.items():
            key = str(integration_type.value)
            value = str(user_id)
            authorizer_user_ids_data[key] = value
    
    data['authorizing_integration_owners'] = authorizer_user_ids_data
    return data


def validate_authorizer_user_ids(authorizer_user_ids):
    """
    Validates the authorizer user identifiers.
    
    Parameters
    ----------
    authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int, ClientUserBase | int>`
        Authorizer user identifiers to validate.
    
    Returns
    -------
    authorizer_user_ids : `None | dict<ApplicationIntegrationType, int>`
    
    Raises
    ------
    TypeError
        - Value of invalid type given.
    """
    if authorizer_user_ids is None:
        return None
    
    if not isinstance(authorizer_user_ids, dict):
        raise TypeError(
            f'`authorizer_user_ids` can be `None`,'
            f'`dict<{ApplicationIntegrationType.__name__} | {ApplicationIntegrationType.VALUE_TYPE.__name__}, '
            f'int | {ClientUserBase.__name__}, got '
            f'{type(authorizer_user_ids).__name__}; {authorizer_user_ids!r}.'
        )
    
    if not authorizer_user_ids:
        return None
    
    validated_authorizer_user_ids = {}
    
    for key, value in authorizer_user_ids.items():
        if isinstance(key, ApplicationIntegrationType):
            integration_type = key
        
        elif isinstance(key, ApplicationIntegrationType.VALUE_TYPE):
            integration_type = ApplicationIntegrationType.get(key)
        
        else:
            raise TypeError(
                f'`authorizer_user_ids` keys can be '
                f'`{ApplicationIntegrationType.__name__}`, `{ApplicationIntegrationType.VALUE_TYPE.__name__}`, '
                f'got {type(key).__name__}; {key!r}; '
                f'authorizer_user_ids = {authorizer_user_ids!r}.'
            )
        
        if isinstance(value, int):
            user_id = value
        
        elif isinstance(value, ClientUserBase):
            user_id = value.id
        
        else:
            raise TypeError(
                f'`authorizer_user_ids` values can be `int`, `{ClientUserBase.__name__}`, '
                f'got {type(value).__name__}; {value!r}; '
                f'authorizer_user_ids = {authorizer_user_ids!r}.'
            )
        
        validated_authorizer_user_ids[integration_type] = user_id
    
    return validated_authorizer_user_ids


# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('message_interaction_id')


# interacted_message_id

parse_interacted_message_id = entity_id_parser_factory('interacted_message_id')
put_interacted_message_id_into = entity_id_optional_putter_factory('interacted_message_id')
validate_interacted_message_id = entity_id_validator_factory('interacted_message_id', NotImplemented, include = 'Message')


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


# response_message_id

parse_response_message_id = entity_id_parser_factory('original_response_message_id')
put_response_message_id_into = entity_id_optional_putter_factory('original_response_message_id')
validate_response_message_id = entity_id_validator_factory('response_message_id', NotImplemented, include = 'Message')


# target_message_id

parse_target_message_id = entity_id_parser_factory('target_message_id')
put_target_message_id_into = entity_id_optional_putter_factory('target_message_id')
validate_target_message_id = entity_id_validator_factory('target_message_id', NotImplemented, include = 'Message')


# target_user

parse_target_user = nullable_entity_parser_factory('target_user', User)
put_target_user_into = nullable_entity_optional_putter_factory(
    'target_user', ClientUserBase, force_include_internals = True
)
validate_target_user = nullable_entity_validator_factory('target_user', ClientUserBase)


# triggering_interaction

parse_triggering_interaction = nullable_entity_parser_factory(
    'triggering_interaction_metadata', NotImplemented, include = 'MessageInteraction'
)
put_triggering_interaction_into = nullable_entity_optional_putter_factory(
    'triggering_interaction_metadata', NotImplemented, can_include_internals = True, include = 'MessageInteraction',
)
validate_triggering_interaction = nullable_entity_validator_factory(
    'triggering_interaction', NotImplemented, include = 'MessageInteraction'
)


# type

parse_type = preinstanced_parser_factory(
    'type', NotImplemented, NotImplemented, include = 'InteractionType', include_default_attribute_name = 'none'
)

put_type_into = preinstanced_putter_factory('type')

validate_type = preinstanced_validator_factory('type', NotImplemented, include = 'InteractionType')


# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER, force_include_internals = True)
validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)
