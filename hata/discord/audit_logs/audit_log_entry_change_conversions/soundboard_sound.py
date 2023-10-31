__all__ = ()

from ...emoji import create_partial_emoji_data, create_partial_emoji_from_data
from ...soundboard.soundboard_sound.fields import validate_available, validate_emoji, validate_name, validate_volume

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_name, put_converter_name


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

EMOJI_CONVERSION = AuditLogEntryChangeConversion(
    'emoji',
    'emoji',
    FLAG_IS_MODIFICATION,
    validator = validate_emoji,
)


@EMOJI_CONVERSION.set_get_converter
def emoji_get_converter(value):
    if (value is not None):
        value = create_partial_emoji_from_data(value)
    
    return value


@EMOJI_CONVERSION.set_put_converter
def emoji_put_converter(value):
    if value is not None:
        value = create_partial_emoji_data(value)
    
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
    EMOJI_CONVERSION,
    NAME_CONVERSION,
    VOLUME_CONVERSION,
)
