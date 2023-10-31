__all__ = ()


from ...soundboard.soundboard_sound.fields import (
    validate_available, validate_user_id, validate_id, validate_name, validate_volume
)

from ..audit_log_change.flags import FLAG_IS_IGNORED, FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name


# ---- available ----

AVAILABLE_CONVERSION = AuditLogEntryChangeConversion(
    'available',
    'available',
    FLAG_IS_MODIFICATION,
    validator = validate_available,
)


@AVAILABLE_CONVERSION.set_get_converter
def available_get_converter(value):
    if value is None:
        value = True
    return value


# ---- emoji ----
# Need to add support for this as well
# EMOJI_CONVERSION_0 = AuditLogEntryChangeConversion(
#     'emoji_id',
#     'emoji',
#     FLAG_IS_MODIFICATION,
#     validator = validate_emoji,
# )
#
#
# EMOJI_CONVERSION1 = AuditLogEntryChangeConversion(
#     'emoji_name',
#     'emoji',
#     FLAG_IS_MODIFICATION,
#     validator = validate_emoji,
# )

# ---- id  ----

ID_CONVERSION = AuditLogEntryChangeConversion(
    'sound_id',
    'id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_id,
)


ID_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    'id',
    '',
    FLAG_IS_IGNORED,
)

# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)

# ---- user_id ----

USER_ID_CONVERSION = AuditLogEntryChangeConversion(
    'user_id',
    'user_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_user_id,
)


# ---- volume ----

VOLUME_CONVERSION = AuditLogEntryChangeConversion(
    'volume',
    'volume',
    FLAG_IS_MODIFICATION,
    validator = validate_volume,
)


@VOLUME_CONVERSION.set_get_converter
def volume_get_converter(value):
    if (value is None):
        value = 1.0
    
    return value


# ---- Construct ----

SOUNDBOARD_SOUND_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVAILABLE_CONVERSION,
    ID_CONVERSION,
    ID_CONVERSION_IGNORED,
    NAME_CONVERSION,
    USER_ID_CONVERSION,
    VOLUME_CONVERSION,
)
