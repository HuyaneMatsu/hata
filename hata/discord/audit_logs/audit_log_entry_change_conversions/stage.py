__all__ = ()

from ...scheduled_event import PrivacyLevel
from ...stage.stage.fields import validate_privacy_level, validate_topic

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_description, put_converter_description


# ---- privacy_level ----

PRIVACY_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    'privacy_level',
    'privacy_level',
    FLAG_IS_MODIFICATION,
    validator = validate_privacy_level,
)


@PRIVACY_LEVEL_CONVERSION.set_get_converter
def privacy_level_get_converter(value):
    return PrivacyLevel.get(value)


@PRIVACY_LEVEL_CONVERSION.set_put_converter
def privacy_level_put_converter(value):
    return value.value


# ---- topic ----

TOPIC_CONVERSION = AuditLogEntryChangeConversion(
    'topic',
    'topic',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_topic,
)


# ---- Construct ----

STAGE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    PRIVACY_LEVEL_CONVERSION,
    TOPIC_CONVERSION,
)
