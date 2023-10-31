__all__ = ()

from ...integration import IntegrationExpireBehavior
from ...integration.integration_metadata.constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ...integration.integration_metadata.fields import (
    validate_emojis_enabled, validate_expire_behavior, validate_expire_grace_period
)

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup


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


# ---- Construct ----

INTEGRATION_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    EMOJIS_ENABLED_CONVERSION,
    EXPIRE_BEHAVIOR_CONVERSION,
    EXPIRE_GRACE_PERIOD_CONVERSION,
)
