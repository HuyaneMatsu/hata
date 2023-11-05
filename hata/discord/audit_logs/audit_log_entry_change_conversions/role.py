__all__ = ()

from ...bases import Icon
from ...color import Color
from ...emoji import create_unicode_emoji
from ...permission import Permission
from ...permission.constants import PERMISSION_KEY
from ...role import RoleFlag
from ...role.role.fields import (
    validate_color, validate_flags, validate_mentionable, validate_name, validate_permissions, validate_position,
    validate_separated, validate_unicode_emoji
)
from ...role.role.role import ROLE_ICON

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_name, put_converter_name


# ---- color ----

COLOR_CONVERSION = AuditLogEntryChangeConversion(
    'color',
    'color',
    FLAG_IS_MODIFICATION,
    validator = validate_color,
)


@COLOR_CONVERSION.set_get_converter
def color_get_converter(value):
    if value is None:
        value = Color()
    else:
        value = Color(value)
    
    return value


@COLOR_CONVERSION.set_put_converter
def color_put_converter(value):
    return int(value)


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    'flags',
    'flags',
    FLAG_IS_MODIFICATION,
    validator = validate_flags,
)


@FLAGS_CONVERSION.set_get_converter
def flags_get_converter(value):
    if value is None:
        value = RoleFlag()
    else:
        value = RoleFlag(value)
    
    return value


@FLAGS_CONVERSION.set_put_converter
def flags_put_converter(value):
    return int(value)


# ---- icon ----

ICON_CONVERSION = AuditLogEntryChangeConversion(
    'icon_hash',
    'icon',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash.fget,
    validator = ROLE_ICON.validate_icon,
)


# ---- mentionable ----

MENTIONABLE_CONVERSION = AuditLogEntryChangeConversion(
    'mentionable',
    'mentionable',
    FLAG_IS_MODIFICATION,
    validator = validate_mentionable,
)


@MENTIONABLE_CONVERSION.set_get_converter
def mentionable_get_converter(value):
    if value is None:
        value = False

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


# ---- permissions ----

PERMISSIONS_CONVERSION = AuditLogEntryChangeConversion(
    PERMISSION_KEY,
    'permissions',
    FLAG_IS_MODIFICATION,
    validator = validate_permissions,
)


@PERMISSIONS_CONVERSION.set_get_converter
def permission_get_converter(value):
    if value is None:
        value = Permission()
    else:
        value = Permission(value)
    return value


@PERMISSIONS_CONVERSION.set_put_converter
def permission_put_converter(value):
    return format(value, 'd')


# ---- position ----

POSITION_CONVERSION = AuditLogEntryChangeConversion(
    'position',
    'position',
    FLAG_IS_MODIFICATION,
    validator = validate_position,
)

@POSITION_CONVERSION.set_get_converter
def position_get_converter(value):
    if value is None:
        value = 0
    return value


# ---- separated ----

SEPARATED_CONVERSION = AuditLogEntryChangeConversion(
    'hoist',
    'separated',
    FLAG_IS_MODIFICATION,
    validator = validate_separated,
)


@SEPARATED_CONVERSION.set_get_converter
def separated_get_converter(value):
    if value is None:
        value = False

    return value


# ---- unicode_emoji ----

UNICODE_EMOJI_CONVERSION = AuditLogEntryChangeConversion(
    'unicode_emoji',
    'unicode_emoji',
    FLAG_IS_MODIFICATION,
    validator = validate_unicode_emoji,
)

@UNICODE_EMOJI_CONVERSION.set_get_converter
def position_get_converter(value):
    if (value is not None):
        value = create_unicode_emoji(value)
    
    return value


@UNICODE_EMOJI_CONVERSION.set_put_converter
def position_put_converter(value):
    if (value is not None):
        value = value.unicode
    
    return value


# ---- Construct ----

ROLE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    COLOR_CONVERSION,
    FLAGS_CONVERSION,
    ICON_CONVERSION,
    MENTIONABLE_CONVERSION,
    NAME_CONVERSION,
    PERMISSIONS_CONVERSION,
    POSITION_CONVERSION,
    SEPARATED_CONVERSION,
    UNICODE_EMOJI_CONVERSION,
)
