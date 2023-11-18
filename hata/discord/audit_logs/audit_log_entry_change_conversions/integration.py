__all__ = ()

from ...integration import IntegrationExpireBehavior, IntegrationType
from ...integration.integration.fields import validate_name, validate_type
from ...integration.integration_metadata.constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ...integration.integration_metadata.fields import (
    validate_emojis_enabled, validate_expire_behavior, validate_expire_grace_period
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_name, value_serializer_name


# ---- emojis_enabled ----

EMOJIS_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    ('enable_emoticons',),
    'emojis_enabled',
    value_validator = validate_emojis_enabled,
)


@EMOJIS_ENABLED_CONVERSION.set_value_deserializer
def emojis_enabled_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- expire_behavior ----

EXPIRE_BEHAVIOR_CONVERSION = AuditLogEntryChangeConversion(
    ('expire_behavior',),
    'expire_behavior',
    value_validator = validate_expire_behavior,
)


@EXPIRE_BEHAVIOR_CONVERSION.set_value_deserializer
def expire_behavior_value_deserializer(value):
    return IntegrationExpireBehavior.get(value)


@EXPIRE_BEHAVIOR_CONVERSION.set_value_serializer
def expire_behavior_value_serializer(value):
    return value.value


# ---- expire_grace_period ----

EXPIRE_GRACE_PERIOD_CONVERSION = AuditLogEntryChangeConversion(
    ('expire_grace_period',),
    'expire_grace_period',
    value_validator = validate_expire_grace_period,
)

@EXPIRE_GRACE_PERIOD_CONVERSION.set_value_deserializer
def expire_grace_period_value_deserializer(value):
    if value is None:
        value = EXPIRE_GRACE_PERIOD_DEFAULT
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('type',),
    'type',
    value_validator = validate_type,
)


@TYPE_CONVERSION.set_value_deserializer
def type_value_deserializer(value):
    return IntegrationType.get(value)


@TYPE_CONVERSION.set_value_serializer
def type_value_serializer(value):
    return value.value


# ---- Construct ----

INTEGRATION_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    EMOJIS_ENABLED_CONVERSION,
    EXPIRE_BEHAVIOR_CONVERSION,
    EXPIRE_GRACE_PERIOD_CONVERSION,
    NAME_CONVERSION,
    TYPE_CONVERSION,
)
