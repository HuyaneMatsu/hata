__all__ = ()

from ...sticker import StickerFormat, StickerType
from ...sticker.sticker.constants import SORT_VALUE_MIN
from ...sticker.sticker.fields import (
    validate_available, validate_description, validate_format, validate_guild_id, validate_id, validate_name,
    validate_sort_value, validate_tags, validate_type
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import change_deserializer_deprecation
from ..conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_name, value_serializer_description, value_serializer_id,
    value_serializer_name
)

# ---- asset ----

ASSET_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('asset',),
    '',
    change_deserializer = change_deserializer_deprecation,
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


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    ('description',),
    'description',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_description,
)


# ---- format ----

FORMAT_CONVERSION = AuditLogEntryChangeConversion(
    ('format_type',),
    'format',
    value_validator = validate_format,
)


@FORMAT_CONVERSION.set_value_deserializer
def format_value_deserializer(value):
    return StickerFormat(value)


@FORMAT_CONVERSION.set_value_serializer
def format_value_serializer(value):
    return value.value


# ---- guild_id ----

GUILD_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('guild_id',),
    'guild_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_guild_id,
)


# ---- id ----

ID_CONVERSION = AuditLogEntryChangeConversion(
    ('id',),
    'id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_id,
)


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- sort_value ----

SORT_VALUE_CONVERSION = AuditLogEntryChangeConversion(
    ('sort_value',),
    'sort_value',
    value_validator = validate_sort_value,
)


@SORT_VALUE_CONVERSION.set_value_deserializer
def sort_value_value_deserializer(value):
    if value is None:
        value = SORT_VALUE_MIN
    return value


# ---- tags ----

TAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('tags',),
    'tags',
    value_validator = validate_tags,
)


@TAGS_CONVERSION.set_value_deserializer
def tags_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = frozenset(value.split(', '))
    
    return value


@TAGS_CONVERSION.set_value_serializer
def tags_value_serializer(value):
    if value is None:
       value = ''
    else:
        value = ', '.join(sorted(value))
    
    return value


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('type',),
    'type',
    value_validator = validate_type,
)


@TYPE_CONVERSION.set_value_deserializer
def type_value_deserializer(value):
    return StickerType(value)


@TYPE_CONVERSION.set_value_serializer
def type_value_serializer(value):
    return value.value


# ---- Construct ----

STICKER_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    ASSET_CONVERSION_IGNORED,
    AVAILABLE_CONVERSION,
    DESCRIPTION_CONVERSION,
    FORMAT_CONVERSION,
    GUILD_ID_CONVERSION,
    ID_CONVERSION,
    NAME_CONVERSION,
    SORT_VALUE_CONVERSION,
    TAGS_CONVERSION,
    TYPE_CONVERSION,
)
