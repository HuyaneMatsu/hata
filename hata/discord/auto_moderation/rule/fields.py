__all__ = ()

from ...channel import Channel
from ...field_parsers import (
    bool_parser_factory, entity_id_array_parser_factory, entity_id_parser_factory, force_string_parser_factory,
    nullable_object_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    force_string_putter_factory, optional_entity_id_array_optional_putter_factory,
    nullable_object_array_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_array_validator_factory, entity_id_validator_factory,
    force_string_validator_factory, nullable_object_array_validator_factory, preinstanced_validator_factory
)
from ...role import Role
from ...user import ClientUserBase

from ..action import AutoModerationAction
from ..trigger_metadata import AutoModerationRuleTriggerMetadataBase

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType


# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('rule_id')

# actions

parse_actions = nullable_object_array_parser_factory('actions', AutoModerationAction)
put_actions_into = nullable_object_array_optional_putter_factory('actions')
validate_actions = nullable_object_array_validator_factory('actions', AutoModerationAction)

# creator_id

parse_creator_id = entity_id_parser_factory('creator_id')
put_creator_id_into = entity_id_optional_putter_factory('creator_id')
validate_creator_id = entity_id_validator_factory('creator_id', ClientUserBase)

# enabled

parse_enabled = bool_parser_factory('enabled', True)
put_enabled_into = bool_optional_putter_factory('enabled', True)
validate_enabled = bool_validator_factory('enabled', True)

# event_type

parse_event_type = preinstanced_parser_factory('event_type', AutoModerationEventType, AutoModerationEventType.none)
put_event_type_into = preinstanced_putter_factory('event_type')
validate_event_type = preinstanced_validator_factory('event_type', AutoModerationEventType)

# excluded_channel_ids

parse_excluded_channel_ids = entity_id_array_parser_factory('exempt_channels')
put_excluded_channel_ids_into = optional_entity_id_array_optional_putter_factory('exempt_channels')
validate_excluded_channel_ids = entity_id_array_validator_factory('excluded_channel_ids', Channel)

# excluded_role_ids

parse_excluded_role_ids = entity_id_array_parser_factory('exempt_roles')
put_excluded_role_ids_into = optional_entity_id_array_optional_putter_factory('exempt_roles')
validate_excluded_role_ids = entity_id_array_validator_factory('excluded_role_ids', Role)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', include = 'Guild')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# trigger_type

parse_trigger_type = preinstanced_parser_factory(
    'trigger_type', AutoModerationRuleTriggerType, AutoModerationRuleTriggerType.none
)
put_trigger_type_into = preinstanced_putter_factory('trigger_type')
validate_trigger_type = preinstanced_validator_factory('trigger_type', AutoModerationRuleTriggerType)

# trigger_metadata

def parse_trigger_metadata(data, rule_trigger_type):
    """
    Parsers out an auto moderation rule's trigger metadata form the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Auto moderation rule data.
    
    rule_trigger_type : ``AutoModerationRuleTriggerType``
        The rule trigger's type.
    
    Returns
    -------
    trigger_metadata : ``AutoModerationRuleTriggerMetadataBase``
    """
    trigger_metadata_type = rule_trigger_type.metadata_type
    trigger_metadata_data = data.get('trigger_metadata', None)
    
    if trigger_metadata_data is None:
        trigger_metadata = trigger_metadata_type()
    else:
        trigger_metadata = trigger_metadata_type.from_data(trigger_metadata_data)
    
    return trigger_metadata


def put_trigger_metadata_into(trigger_metadata, data, defaults):
    """
    Puts the given rule trigger metadata's data into the given `data` json serializable object.
    
    Parameters
    ----------
    trigger_metadata : ``AutoModerationRuleTriggerMetadataBase``
        Rule trigger metadata.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (type(trigger_metadata) is not AutoModerationRuleTriggerMetadataBase):
        data['trigger_metadata'] = trigger_metadata.to_data(defaults = defaults)
    
    return data
