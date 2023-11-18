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

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_name, value_serializer_name


# ---- color ----

COLOR_CONVERSION = AuditLogEntryChangeConversion(
    ('color',),
    'color',
    value_validator = validate_color,
)


@COLOR_CONVERSION.set_value_deserializer
def color_value_deserializer(value):
    if value is None:
        value = Color()
    else:
        value = Color(value)
    
    return value


@COLOR_CONVERSION.set_value_serializer
def color_value_serializer(value):
    return int(value)


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('flags',),
    'flags',
    value_validator = validate_flags,
)


@FLAGS_CONVERSION.set_value_deserializer
def flags_value_deserializer(value):
    if value is None:
        value = RoleFlag()
    else:
        value = RoleFlag(value)
    
    return value


@FLAGS_CONVERSION.set_value_serializer
def flags_value_serializer(value):
    return int(value)


# ---- icon ----

ICON_CONVERSION = AuditLogEntryChangeConversion(
    ('icon_hash',),
    'icon',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = ROLE_ICON.validate_icon,
)


# ---- mentionable ----

MENTIONABLE_CONVERSION = AuditLogEntryChangeConversion(
    ('mentionable',),
    'mentionable',
    value_validator = validate_mentionable,
)


@MENTIONABLE_CONVERSION.set_value_deserializer
def mentionable_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- permissions ----

PERMISSIONS_CONVERSION = AuditLogEntryChangeConversion(
    (PERMISSION_KEY,),
    'permissions',
    value_validator = validate_permissions,
)


@PERMISSIONS_CONVERSION.set_value_deserializer
def permission_value_deserializer(value):
    if value is None:
        value = Permission()
    else:
        value = Permission(value)
    return value


@PERMISSIONS_CONVERSION.set_value_serializer
def permission_value_serializer(value):
    return format(value, 'd')


# ---- position ----

POSITION_CONVERSION = AuditLogEntryChangeConversion(
    ('position',),
    'position',
    value_validator = validate_position,
)

@POSITION_CONVERSION.set_value_deserializer
def position_value_deserializer(value):
    if value is None:
        value = 0
    return value


# ---- separated ----

SEPARATED_CONVERSION = AuditLogEntryChangeConversion(
    ('hoist',),
    'separated',
    value_validator = validate_separated,
)


@SEPARATED_CONVERSION.set_value_deserializer
def separated_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- unicode_emoji ----

UNICODE_EMOJI_CONVERSION = AuditLogEntryChangeConversion(
    ('unicode_emoji',),
    'unicode_emoji',
    value_validator = validate_unicode_emoji,
)

@UNICODE_EMOJI_CONVERSION.set_value_deserializer
def position_value_deserializer(value):
    if (value is not None):
        value = create_unicode_emoji(value)
    
    return value


@UNICODE_EMOJI_CONVERSION.set_value_serializer
def position_value_serializer(value):
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
