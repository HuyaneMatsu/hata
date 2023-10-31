__all__ = ()

from ...emoji.emoji.fields import validate_available, validate_name, validate_role_ids

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_ids, get_converter_name, put_converter_ids, put_converter_name
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


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- role_ids ----

ROLE_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'roles',
    'role_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_role_ids,
)


# ---- Construct ----

EMOJI_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVAILABLE_CONVERSION,
    NAME_CONVERSION,
    ROLE_IDS_CONVERSION,
)
