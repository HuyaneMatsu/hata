__all__ = ()

from ...application_command import ApplicationCommand
from ...application_command.constants import APPLICATION_COMMAND_NAME_LENGTH_MAX, APPLICATION_COMMAND_NAME_LENGTH_MIN
from ...bases import DiscordEntity
from ...component import ComponentType
from ...component.shared_constants import CUSTOM_ID_LENGTH_MAX
from ...field_parsers import (
    entity_id_parser_factory, force_string_parser_factory, nullable_object_array_parser_factory,
    nullable_string_array_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, entity_id_putter_factory, force_string_putter_factory,
    nullable_object_array_optional_putter_factory, nullable_string_array_optional_putter_factory,
    preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_entity_validator_factory,
    nullable_object_array_validator_factory, nullable_string_array_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)

from ..interaction_component import InteractionComponent
from ..interaction_option import InteractionOption
from ..resolved import Resolved

# component_type

parse_component_type = preinstanced_parser_factory('component_type', ComponentType, ComponentType.none)
put_component_type_into = preinstanced_putter_factory('component_type')
validate_component_type = preinstanced_validator_factory('component_type', ComponentType)

# components

parse_components = nullable_object_array_parser_factory('components', InteractionComponent)
put_components_into = nullable_object_array_optional_putter_factory('components')
validate_components = nullable_object_array_validator_factory('components', InteractionComponent)

# custom_id

parse_custom_id = nullable_string_parser_factory('custom_id')
put_custom_id_into = url_optional_putter_factory('custom_id')
validate_custom_id = nullable_string_validator_factory('custom_id', 0, CUSTOM_ID_LENGTH_MAX)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id', ApplicationCommand)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory(
    'name', APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX
)

# options

parse_options = nullable_object_array_parser_factory('options', InteractionOption)
put_options_into = nullable_object_array_optional_putter_factory('options')
validate_options = nullable_object_array_validator_factory('options', InteractionOption)

# resolved

def parse_resolved(data, interaction_event):
    """
    Parsers out a resolved object from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Interaction metadata data.
    
    interaction_event : ``InteractionEvent``
        Parent interaction event instance.
    
    Returns
    -------
    resolved : `None`, ``Resolved``
    """
    resolved_data = data.get('resolved', None)
    if (resolved_data is not None) and resolved_data:
        return Resolved.from_data(resolved_data, interaction_event)


def put_resolved_into(resolved, data, defaults, *, interaction_event = None):
    """
    Puts the given `resolved` into the given interaction metadata data.
    
    Parameters
    ----------
    resolved  : `None`, ``Resolved``
        
    data : `dict` of (`str`, `object`) items
        Interaction metadata data.
    
    defaults : `bool`
        Whether default field values should be included as well.
    
    interaction_event : ``InteractionEvent`` = `None`, Optional (Keyword only)
        The respective guild's identifier to use for handing user guild profiles.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    # Cpython devs: "We do not need goto in python".
    # Also them: *uSeS gOtO TwIcE iN EveRy C fUnCTiOn*.
    while True:
        if (resolved is None):
            if not defaults:
                break
            
            resolved_data = {}
        
        else:
            resolved_data = resolved.to_data(defaults = defaults, interaction_event = interaction_event)
        
        data['resolved'] = resolved_data
        break
    
    return data


validate_resolved = nullable_entity_validator_factory('resolved', Resolved)

# target_id

parse_target_id = entity_id_parser_factory('target_id')
put_target_id_into = entity_id_optional_putter_factory('target_id')
validate_target_id = entity_id_validator_factory('target_id', DiscordEntity)

# values

parse_values = nullable_string_array_parser_factory('values')
put_values_into = nullable_string_array_optional_putter_factory('values')
validate_values = nullable_string_array_validator_factory('values')
