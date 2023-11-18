__all__ = ()

from ...bases import Icon
from ...user.user.fields import validate_name
from ...user.user.user_base import USER_AVATAR
from ...webhook import WebhookType
from ...webhook.webhook.fields import validate_application_id, validate_channel_id, validate_type

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name


# ---- application_id ----

APPLICATION_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('application_id',),
    'application_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_application_id,
)

# ---- avatar ----

AVATAR_CONVERSION = AuditLogEntryChangeConversion(
    ('avatar_hash',),
    'avatar',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = USER_AVATAR.validate_icon,
)


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('channel_id',),
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


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
    return WebhookType.get(value)


@TYPE_CONVERSION.set_value_serializer
def type_value_serializer(value):
    return value.value


# ---- Construct ----

WEBHOOK_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    APPLICATION_ID_CONVERSION,
    AVATAR_CONVERSION,
    CHANNEL_ID_CONVERSION,
    NAME_CONVERSION,
    TYPE_CONVERSION,
)
