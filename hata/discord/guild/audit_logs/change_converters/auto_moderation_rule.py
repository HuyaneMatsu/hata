__all__ = ()

from ....auto_moderation import AutoModerationAction, AutoModerationEventType, AutoModerationRuleTriggerType
from ....auto_moderation.trigger_metadata.utils import try_get_auto_moderation_trigger_metadata_type_from_data

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_nothing, convert_snowflake, convert_snowflake_array


def convert_auto_moderation_rule_actions(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        if before:
            before = tuple(AutoModerationAction(data) for data in before)
        else:
            before = None
    
    after = data.get('new_value', None)
    if (after is not None):
        if after:
            after = tuple(AutoModerationAction(data) for data in after)
        else:
            after = None
    
    return AuditLogChange('actions', before, after)


def convert_auto_moderation_rule_event_type(name, data):
    return _convert_preinstanced('event_type', data, AutoModerationEventType)


def convert_snowflake_array__excluded_channel_ids(name, data):
    return convert_snowflake_array('excluded_channel_ids', data)


def convert_snowflake_array__excluded_role_ids(name, data):
    return convert_snowflake_array('excluded_role_ids', data)


def convert_auto_moderation_trigger_entity_metadata(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        metadata_type = try_get_auto_moderation_trigger_metadata_type_from_data(before)
        if metadata_type is None:
            before = None
        else:
            before = metadata_type.from_data(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        metadata_type = try_get_auto_moderation_trigger_metadata_type_from_data(after)
        if metadata_type is None:
            after = None
        else:
            after = metadata_type.from_data(after)
    
    return AuditLogChange('trigger_metadata', before, after)


def convert_auto_moderation_rule_trigger_type(name, data):
    return _convert_preinstanced('trigger_type', data, AutoModerationRuleTriggerType)


AUTO_MODERATION_RULE_CONVERTERS = {
    'actions': convert_auto_moderation_rule_actions,
    'creator_id': convert_snowflake,
    'enabled': convert_nothing,
    'event_type': convert_auto_moderation_rule_event_type,
    'exempt_channels': convert_snowflake_array__excluded_channel_ids,
    'exempt_roles': convert_snowflake_array__excluded_role_ids,
    'name': convert_nothing,
    'trigger_metadata': convert_auto_moderation_trigger_entity_metadata,
    'trigger_type': convert_auto_moderation_rule_trigger_type
}
