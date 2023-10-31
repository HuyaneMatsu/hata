__all__ = ()

from ...auto_moderation import AutoModerationRuleTriggerType
from ...auto_moderation.execution_event.fields import validate_channel_id
from ...auto_moderation.rule.fields import validate_name, validate_trigger_type

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'channel_id',
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_channel_id,
)


# ---- rule_name ----

RULE_NAME_CONVERSION = AuditLogEntryDetailConversion(
    'auto_moderation_rule_name',
    'rule_name',
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- trigger_type ----

TRIGGER_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'auto_moderation_rule_trigger_type', 'trigger_type', validator = validate_trigger_type
)


@TRIGGER_TYPE_CONVERSION.set_get_converter
def trigger_type_get_converter(value):
    return AutoModerationRuleTriggerType.get(value)


@TRIGGER_TYPE_CONVERSION.set_put_converter
def trigger_type_put_converter(value):
    return value.value


# ---- Construct ----

AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
    RULE_NAME_CONVERSION,
    TRIGGER_TYPE_CONVERSION,
)
