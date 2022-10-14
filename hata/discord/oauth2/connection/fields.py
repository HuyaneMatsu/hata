__all__ = ()

from scarletio import include

from ...field_parsers import bool_parser_factory, force_string_parser_factory, preinstanced_parser_factory
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, preinstanced_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import bool_validator_factory, force_string_validator_factory, preinstanced_validator_factory

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import ConnectionType, ConnectionVisibility


Integration = include('Integration')

# parse_friend_sync

parse_friend_sync = bool_parser_factory('friend_sync', False)
put_friend_sync_into = bool_optional_putter_factory('friend_sync', False)
validate_friend_sync = bool_validator_factory('friend_sync')

# integrations

def parse_integrations(data):
    """
    Parses out an integration array from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Entity data.
    
    Returns
    -------
    entity_array : `None`, `tuple` of ``Integration``
    """
    entity_data_array = data.get('integrations', None)
    if (entity_data_array is None) or (not entity_data_array):
        entity_array = None
    else:
        entity_array = tuple(sorted(Integration.from_data(entity_data) for entity_data in entity_data_array))
    
    return entity_array


def put_integrations_into(entity_array, data, defaults, *, include_internals = False):
    """
    Puts the given integration array into the given `data` json serializable object.
    
    Parameters
    ----------
    entity_array : `None`, `tuple` of ``Integration``
        Integration array.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    include_internals : `bool` = `False`, Optional (Keyword only)
        Whether internal fields should be included.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if entity_array is None:
        entity_data_array = []
    else:
        entity_data_array = [
            entity.to_data(defaults = defaults, include_internals = include_internals)
            for entity in entity_array
        ]
    
    data['integrations'] = entity_data_array
    
    return data


def validate_integrations(entity_array):
    """
    Validates the given nullable entity array field.
    
    Parameters
    ----------
    entity_array : `None`, `iterable` of ``Integration``
        The entity array to validate.
    
    Returns
    -------
    entity_array : `None`, `tuple` of ``Integration``
    
    Raises
    ------
    TypeError
        - If `entity_array` is not `None`, `iterable` of ``Integration``.
    """
    if entity_array is None:
        return None
    
    if (getattr(entity_array, '__iter__', None) is None):
        raise TypeError(
            f'`integrations` can be `None`, `iterable` of `{Integration.__name__}`, got '
            f'{entity_array.__class__.__name__}; {entity_array!r}.'
        )
        
    entity_array_processed = None
    
    for entity in entity_array:
        if not isinstance(entity, Integration):
            raise TypeError(
                f'`integrations` can contain `{Integration.__name__}` elements, got '
                f'{entity.__class__.__name__}; {entity!r}; entity_array = {entity_array!r}.'
            )
        
        if (entity_array_processed is None):
            entity_array_processed = set()
        
        entity_array_processed.add(entity)
    
    if (entity_array_processed is not None):
        entity_array_processed = tuple(sorted(entity_array_processed))
    
    return entity_array_processed

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# revoked

parse_revoked = bool_parser_factory('revoked', False)
put_revoked_into = bool_optional_putter_factory('revoked', False)
validate_revoked = bool_validator_factory('revoked')

# show_activity

parse_show_activity = bool_parser_factory('show_activity', False)
put_show_activity_into = bool_optional_putter_factory('show_activity', False)
validate_show_activity = bool_validator_factory('show_activity')

# two_way_link

parse_two_way_link = bool_parser_factory('two_way_link', False)
put_two_way_link_into = bool_optional_putter_factory('two_way_link', False)
validate_two_way_link = bool_validator_factory('two_way_link')

# type

parse_type = preinstanced_parser_factory('type', ConnectionType, ConnectionType.unknown)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ConnectionType)

# verified

parse_verified = bool_parser_factory('verified', False)
put_verified_into = bool_optional_putter_factory('verified', False)
validate_verified = bool_validator_factory('verified')

# visibility

parse_visibility = preinstanced_parser_factory('visibility', ConnectionVisibility, ConnectionVisibility.user_only)
put_visibility_into = preinstanced_optional_putter_factory('visibility', ConnectionVisibility.user_only)
validate_visibility = preinstanced_validator_factory('visibility', ConnectionVisibility)
