__all__ = ()

from ...bases import Icon
from ...user import GuildProfileFlag
from ...user.guild_profile.fields import (
    validate_bypasses_verification, validate_flags, validate_nick, validate_pending, validate_timed_out_until
)
from ...user.guild_profile.guild_profile import GUILD_PROFILE_AVATAR
from ...user.voice_state.fields import validate_deaf, validate_mute
from ...utils import datetime_to_timestamp, timestamp_to_datetime

from ..audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_role import AuditLogRole
from ..conversion_helpers.converters import get_converter_description, put_converter_description


# ---- avatar ----

AVATAR_CONVERSION = AuditLogEntryChangeConversion(
    'avatar_hash',
    'avatar',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = GUILD_PROFILE_AVATAR.validate_icon,
)


# ---- bypasses_verification ----

BYPASSES_VERIFICATION_CONVERSION = AuditLogEntryChangeConversion(
    'bypasses_verification',
    'bypasses_verification',
    FLAG_IS_MODIFICATION,
    validator = validate_bypasses_verification,
)


@BYPASSES_VERIFICATION_CONVERSION.set_get_converter
def bypasses_verification_get_converter(value):
    if value is None:
        value = False

    return value


# ---- deaf ----

DEAF_CONVERSION = AuditLogEntryChangeConversion(
    'deaf',
    'deaf',
    FLAG_IS_MODIFICATION,
    validator = validate_deaf,
)


@DEAF_CONVERSION.set_get_converter
def deaf_get_converter(value):
    if value is None:
        value = False

    return value


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
        value = GuildProfileFlag()
    else:
        value = GuildProfileFlag(value)
    
    return value


@FLAGS_CONVERSION.set_put_converter
def flags_put_converter(value):
    return int(value)


# ---- mute ----

MUTE_CONVERSION = AuditLogEntryChangeConversion(
    'mute',
    'mute',
    FLAG_IS_MODIFICATION,
    validator = validate_mute,
)


@MUTE_CONVERSION.set_get_converter
def mute_get_converter(value):
    if value is None:
        value = False

    return value


# ---- nick ----

NICK_CONVERSION = AuditLogEntryChangeConversion(
    'nick',
    'nick',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_nick,
)


# ---- pending ----

PENDING_CONVERSION = AuditLogEntryChangeConversion(
    'pending',
    'pending',
    FLAG_IS_MODIFICATION,
    validator = validate_pending,
)


@PENDING_CONVERSION.set_get_converter
def pending_get_converter(value):
    if value is None:
        value = False

    return value


# ---- roles ----

ROLES_CONVERSION__ADDITION = AuditLogEntryChangeConversion(
    '$add',
    'roles',
    FLAG_IS_ADDITION,
)


ROLES_CONVERSION__REMOVAL = AuditLogEntryChangeConversion(
    '$remove',
    'roles',
    FLAG_IS_REMOVAL,
)


@ROLES_CONVERSION__ADDITION.set_get_converter
@ROLES_CONVERSION__REMOVAL.set_get_converter
def roles_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*sorted(AuditLogRole.from_data(role_data) for role_data in value),)
    return value


@ROLES_CONVERSION__ADDITION.set_put_converter
@ROLES_CONVERSION__REMOVAL.set_put_converter
def roles_put_converter(value):
    if value is None:
        value = []
    else:
        value = [role.to_data(defaults = True) for role in value]
    return value


@ROLES_CONVERSION__ADDITION.set_validator
@ROLES_CONVERSION__REMOVAL.set_validator
def roles_validator(value):
    if value is None:
        return None
    
    if (getattr(type(value), '__iter__', None) is None):
        raise TypeError(
            f'`roles` can be `None`, `iterable` of `{AuditLogRole.__name__}`, got {type(value).__name__}, {value!r}.'
        )
    
    roles = None
    for role in value:
        if not isinstance(role, AuditLogRole):
            raise TypeError(
                f'`roles` can contain `{AuditLogRole.__name__}` elements, got {type(role).__name__}; {role!r}; '
                f'roles = {roles!r}.'
            )
        
        if roles is None:
            roles = []
        roles.append(role)
    
    if (roles is not None):
        roles.sort()
        roles = (*roles,)
    
    return roles


# ---- timed_out_until ----

TIMED_OUT_UNTIL_CONVERSION = AuditLogEntryChangeConversion(
    'communication_disabled_until',
    'timed_out_until',
    FLAG_IS_MODIFICATION,
    validator = validate_timed_out_until,
)


@TIMED_OUT_UNTIL_CONVERSION.set_get_converter
def timed_out_until_converter_get(value):
    if (value is not None):
        value = timestamp_to_datetime(value)
    return value


@TIMED_OUT_UNTIL_CONVERSION.set_put_converter
def timed_out_until_converter_put(value):
    if (value is not None):
        value = datetime_to_timestamp(value)
    return value


# ---- Construct ----

USER_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVATAR_CONVERSION,
    BYPASSES_VERIFICATION_CONVERSION,
    DEAF_CONVERSION,
    FLAGS_CONVERSION,
    MUTE_CONVERSION,
    NICK_CONVERSION,
    PENDING_CONVERSION,
    ROLES_CONVERSION__ADDITION,
    ROLES_CONVERSION__REMOVAL,
    TIMED_OUT_UNTIL_CONVERSION,
)
