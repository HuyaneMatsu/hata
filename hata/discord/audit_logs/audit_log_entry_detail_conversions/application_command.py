__all__ = ()

from ...application_command.application_command_permission.fields import validate_application_id, validate_guild_id
from ...application_command.application_command_permission_overwrite.fields import validate_channel_id

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_serializer_id


# ---- application_id ----

APPLICATION_ID_CONVERSION = AuditLogEntryDetailConversion(
    'application_id',
    'application_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_application_id,
)


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


# ---- guild_id ----

GUILD_ID_CONVERSION = AuditLogEntryDetailConversion(
    'guild_id',
    'guild_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_guild_id,
)


# ---- Construct ----

APPLICATION_COMMAND_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    APPLICATION_ID_CONVERSION,
    CHANNEL_ID_CONVERSION,
    GUILD_ID_CONVERSION,
)
