__all__ = ()

from ...soundboard.soundboard_sound.fields import (
    validate_available, validate_emoji, validate_id, validate_name, validate_user_id, validate_volume
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import (
    change_deserializer_deprecation, change_deserializer_flattened_emoji
)
from ..audit_log_entry_change_conversion.change_serializers import change_serializer_flattened_emoji
from ..audit_log_entry_change_conversion.value_mergers import value_merger_replace
from ..conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)


# ---- available ----

AVAILABLE_CONVERSION = AuditLogEntryChangeConversion(
    ('available',),
    'available',
    value_validator = validate_available,
)


@AVAILABLE_CONVERSION.set_value_deserializer
def available_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- emoji ----

EMOJI_CONVERSION = AuditLogEntryChangeConversion(
    ('emoji_id', 'emoji_name'),
    'emoji',
    change_deserializer = change_deserializer_flattened_emoji,
    change_serializer = change_serializer_flattened_emoji,
    value_validator = validate_emoji,
    value_merger = value_merger_replace
)

# ---- id  ----

ID_CONVERSION = AuditLogEntryChangeConversion(
    ('sound_id',),
    'id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_id,
)


ID_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('id',),
    '',
    change_deserializer = change_deserializer_deprecation,
)

# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)

# ---- user_id ----

USER_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('user_id',),
    'user_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_user_id,
)


# ---- volume ----

VOLUME_CONVERSION = AuditLogEntryChangeConversion(
    ('volume',),
    'volume',
    value_validator = validate_volume,
)


@VOLUME_CONVERSION.set_value_deserializer
def volume_value_deserializer(value):
    if (value is None):
        value = 1.0
    
    return value


# ---- Construct ----

SOUNDBOARD_SOUND_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVAILABLE_CONVERSION,
    EMOJI_CONVERSION,
    ID_CONVERSION,
    ID_CONVERSION_IGNORED,
    NAME_CONVERSION,
    USER_ID_CONVERSION,
    VOLUME_CONVERSION,
)
