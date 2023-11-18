__all__ = ()

from ...auto_moderation import AutoModerationRuleTriggerType
from ...auto_moderation.execution_event.fields import validate_channel_id
from ...auto_moderation.rule.fields import validate_name, validate_trigger_type

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


# ---- rule_name ----

RULE_NAME_CONVERSION = AuditLogEntryDetailConversion(
    'auto_moderation_rule_name',
    'rule_name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- trigger_type ----

TRIGGER_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'auto_moderation_rule_trigger_type', 'trigger_type', value_validator = validate_trigger_type
)


@TRIGGER_TYPE_CONVERSION.set_value_deserializer
def trigger_type_value_deserializer(value):
    return AutoModerationRuleTriggerType.get(value)


@TRIGGER_TYPE_CONVERSION.set_value_serializer
def trigger_type_value_serializer(value):
    return value.value


# ---- Construct ----

AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
    RULE_NAME_CONVERSION,
    TRIGGER_TYPE_CONVERSION,
)
