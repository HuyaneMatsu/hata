__all__ = ()

from ...field_parsers import entity_id_parser_factory, nullable_entity_parser_factory
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, nullable_entity_putter_factory
)
from ...field_validators import entity_id_validator_factory, nullable_entity_validator_factory

from ..embedded_activity_location import EmbeddedActivityLocation
from ..embedded_activity_user_state import EmbeddedActivityUserState


# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', NotImplemented, include = 'Application')


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')


# id

parse_id = entity_id_parser_factory('instance_id')
put_id = entity_id_putter_factory('instance_id')
validate_id = entity_id_validator_factory('id')


# launch_id

parse_launch_id = entity_id_parser_factory('launch_id')
put_launch_id = entity_id_putter_factory('launch_id')
validate_launch_id = entity_id_validator_factory('launch_id')


# location

parse_location = nullable_entity_parser_factory('location', EmbeddedActivityLocation)
put_location = nullable_entity_putter_factory('location', EmbeddedActivityLocation)
validate_location = nullable_entity_validator_factory('location', EmbeddedActivityLocation)


# user_states

def parse_user_states(data, user_states, guild_id = 0):
    """
    Parses the embedded activity user states from the given data.
    
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        data to parse from.
    
    user_states : `dict<int, EmbeddedActivityUserState>`
        The embedded activity's current user states.
    
    guild_id : `int` = `0`, Optional
        The respective guild's identifier.
    
    Returns
    -------
    user_states : `dict<int, EmbeddedActivityUserState>`
    """
    # No need to keep old entities, we just want to use the same dictionary.
    user_states.clear()
    
    user_state_datas = data.get('participants', None)
    if (user_state_datas is not None) and user_state_datas:
        for user_state_data in user_state_datas:
            user_state = EmbeddedActivityUserState.from_data(user_state_data, guild_id)
            user_states[user_state.user_id] = user_state
    
    return user_states


def put_user_states(user_states, data, defaults, *, guild_id = 0):
    """
    Parses the embedded activity user states from the given data.
    
    
    Parameters
    ----------
    user_states : `dict<int, EmbeddedActivityUserState>`
        The user states to serialize.
    
    data : `dict<str, object>`
        Data to serialize to.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    guild_id : `int` = `0`, Optional (Keyword only)
        The respective guild's identifier.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    user_states_data = []
    
    for user_state in user_states.values():
        user_states_data.append(user_state.to_data(defaults = defaults, guild_id = guild_id))
    
    data['participants'] = user_states_data
    return data


def validate_user_states(user_states):
    """
    Validates the given user states value.
    
    Parameters
    ----------
    user_states : `None | iterable<EmbeddedActivityUserState> | dict<int, EmbeddedActivityUserState>`
        The field value to validate.
    
    Returns
    -------
    entity_dictionary : `dict<int, EmbeddedActivityUserState>`
    
    Raises
    ------
    TypeError
        - If `user_states`'s or it's elements type is incorrect.
    """
    validated = {}
    
    if user_states is None:
        return validated
    
    if isinstance(user_states, dict):
        iterator = iter(user_states.values())
    
    elif (getattr(user_states, '__iter__', None) is not None):
        iterator = iter(user_states)
    
    else:
        raise TypeError(
            f'`user_states` can be `None`, `dict` of (`int`, `{EmbeddedActivityUserState.__name__}`) items, '
            f'`iterable` of `{EmbeddedActivityUserState.__name__}` items, '
            f'got {type(user_states).__name__}; {user_states!r}.'
        )
    
    for element in iterator:
        if not isinstance(element, EmbeddedActivityUserState):
            raise TypeError(
                f'`user_states` elements can be `{EmbeddedActivityUserState.__name__}`, got {type(element).__name__}; '
                f'{element!r}; user_states = {user_states!r}.'
            )
        
        validated[element.user_id] = element
    
    return validated
