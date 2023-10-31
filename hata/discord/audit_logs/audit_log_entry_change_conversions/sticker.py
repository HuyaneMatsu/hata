__all__ = ()

from ...sticker.sticker.constants import SORT_VALUE_MIN
from ...sticker.sticker.fields import (
    validate_available, validate_description, validate_name, validate_sort_value, validate_tags
)

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_description, get_converter_name, put_converter_description, put_converter_name
)


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


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    'description',
    'description',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_description,
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


# ---- sort_value ----

SORT_VALUE_CONVERSION = AuditLogEntryChangeConversion(
    'sort_value',
    'sort_value',
    FLAG_IS_MODIFICATION,
    validator = validate_sort_value,
)


@SORT_VALUE_CONVERSION.set_get_converter
def sort_value_get_converter(value):
    if value is None:
        value = SORT_VALUE_MIN
    return value


# ---- tags ----

TAGS_CONVERSION = AuditLogEntryChangeConversion(
    'tags',
    'tags',
    FLAG_IS_MODIFICATION,
    validator = validate_tags,
)


@TAGS_CONVERSION.set_get_converter
def tags_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = frozenset(value.split(', '))
    
    return value


@TAGS_CONVERSION.set_put_converter
def tags_put_converter(value):
    if value is None:
       value = ''
    else:
        value = ', '.join(sorted(value))
    
    return value


# ---- Construct ----

STICKER_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVAILABLE_CONVERSION,
    DESCRIPTION_CONVERSION,
    NAME_CONVERSION,
    SORT_VALUE_CONVERSION,
    TAGS_CONVERSION,
)
