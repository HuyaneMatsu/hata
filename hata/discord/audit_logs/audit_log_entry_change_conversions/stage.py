__all__ = ()

from ...scheduled_event import PrivacyLevel
from ...stage.stage.fields import validate_privacy_level, validate_topic

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_description, value_serializer_description


# ---- privacy_level ----

PRIVACY_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('privacy_level',),
    'privacy_level',
    value_validator = validate_privacy_level,
)


@PRIVACY_LEVEL_CONVERSION.set_value_deserializer
def privacy_level_value_deserializer(value):
    return PrivacyLevel.get(value)


@PRIVACY_LEVEL_CONVERSION.set_value_serializer
def privacy_level_value_serializer(value):
    return value.value


# ---- topic ----

TOPIC_CONVERSION = AuditLogEntryChangeConversion(
    ('topic',),
    'topic',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_topic,
)


# ---- Construct ----

STAGE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    PRIVACY_LEVEL_CONVERSION,
    TOPIC_CONVERSION,
)
