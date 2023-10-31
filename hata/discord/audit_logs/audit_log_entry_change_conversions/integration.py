__all__ = ()

from ...integration import IntegrationExpireBehavior, IntegrationType
from ...integration.integration.fields import validate_name, validate_type
from ...integration.integration_metadata.constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ...integration.integration_metadata.fields import (
    validate_emojis_enabled, validate_expire_behavior, validate_expire_grace_period
)

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_name, put_converter_name


# ---- emojis_enabled ----

EMOJIS_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    'enable_emoticons',
    'emojis_enabled',
    FLAG_IS_MODIFICATION,
    validator = validate_emojis_enabled,
)


@EMOJIS_ENABLED_CONVERSION.set_get_converter
def emojis_enabled_get_converter(value):
    if value is None:
        value = True
    return value


# ---- expire_behavior ----

EXPIRE_BEHAVIOR_CONVERSION = AuditLogEntryChangeConversion(
    'expire_behavior',
    'expire_behavior',
    FLAG_IS_MODIFICATION,
    validator = validate_expire_behavior,
)


@EXPIRE_BEHAVIOR_CONVERSION.set_get_converter
def expire_behavior_get_converter(value):
    return IntegrationExpireBehavior.get(value)


@EXPIRE_BEHAVIOR_CONVERSION.set_put_converter
def expire_behavior_put_converter(value):
    return value.value


# ---- expire_grace_period ----

EXPIRE_GRACE_PERIOD_CONVERSION = AuditLogEntryChangeConversion(
    'expire_grace_period',
    'expire_grace_period',
    FLAG_IS_MODIFICATION,
    validator = validate_expire_grace_period,
)

@EXPIRE_GRACE_PERIOD_CONVERSION.set_get_converter
def expire_grace_period_get_converter(value):
    if value is None:
        value = EXPIRE_GRACE_PERIOD_DEFAULT
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'type',
    'type',
    FLAG_IS_MODIFICATION,
    validator = validate_type,
)


@TYPE_CONVERSION.set_get_converter
def type_get_converter(value):
    return IntegrationType.get(value)


@TYPE_CONVERSION.set_put_converter
def type_put_converter(value):
    return value.value


# ---- Construct ----

INTEGRATION_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    EMOJIS_ENABLED_CONVERSION,
    EXPIRE_BEHAVIOR_CONVERSION,
    EXPIRE_GRACE_PERIOD_CONVERSION,
    NAME_CONVERSION,
    TYPE_CONVERSION,
)
