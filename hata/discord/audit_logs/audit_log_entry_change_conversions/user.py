__all__ = ()

from ...bases import Icon
from ...user import GuildProfileFlag
from ...user.guild_profile.fields import (
    validate_bypasses_verification, validate_flags, validate_nick, validate_pending, validate_timed_out_until
)
from ...user.guild_profile.guild_profile import GUILD_PROFILE_AVATAR
from ...user.voice_state.fields import validate_deaf, validate_mute
from ...utils import datetime_to_timestamp, timestamp_to_datetime

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import change_deserializer_addition_and_removal
from ..audit_log_entry_change_conversion.change_serializers import change_serializer_addition_and_removal
from ..audit_log_entry_change_conversion.value_mergers import value_merger_sorted_array
from ..audit_log_role import AuditLogRole
from ..conversion_helpers.converters import value_deserializer_description, value_serializer_description


# ---- avatar ----

AVATAR_CONVERSION = AuditLogEntryChangeConversion(
    ('avatar_hash',),
    'avatar',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = GUILD_PROFILE_AVATAR.validate_icon,
)


# ---- bypasses_verification ----

BYPASSES_VERIFICATION_CONVERSION = AuditLogEntryChangeConversion(
    ('bypasses_verification',),
    'bypasses_verification',
    value_validator = validate_bypasses_verification,
)


@BYPASSES_VERIFICATION_CONVERSION.set_value_deserializer
def bypasses_verification_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- deaf ----

DEAF_CONVERSION = AuditLogEntryChangeConversion(
    ('deaf',),
    'deaf',
    value_validator = validate_deaf,
)


@DEAF_CONVERSION.set_value_deserializer
def deaf_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('flags',),
    'flags',
    value_validator = validate_flags,
)


@FLAGS_CONVERSION.set_value_deserializer
def flags_value_deserializer(value):
    if value is None:
        value = GuildProfileFlag()
    else:
        value = GuildProfileFlag(value)
    
    return value


@FLAGS_CONVERSION.set_value_serializer
def flags_value_serializer(value):
    return int(value)


# ---- mute ----

MUTE_CONVERSION = AuditLogEntryChangeConversion(
    ('mute',),
    'mute',
    value_validator = validate_mute,
)


@MUTE_CONVERSION.set_value_deserializer
def mute_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- nick ----

NICK_CONVERSION = AuditLogEntryChangeConversion(
    ('nick',),
    'nick',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_nick,
)


# ---- pending ----

PENDING_CONVERSION = AuditLogEntryChangeConversion(
    ('pending',),
    'pending',
    value_validator = validate_pending,
)


@PENDING_CONVERSION.set_value_deserializer
def pending_value_deserializer(value):
    if value is None:
        value = False

    return value


# ---- roles ----

ROLES_CONVERSION = AuditLogEntryChangeConversion(
    ('$remove', '$add'),
    'roles',
    change_deserializer = change_deserializer_addition_and_removal,
    change_serializer = change_serializer_addition_and_removal,
    value_merger = value_merger_sorted_array,
)


@ROLES_CONVERSION.set_value_deserializer
def roles_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*sorted(AuditLogRole.from_data(role_data) for role_data in value),)
    return value


@ROLES_CONVERSION.set_value_serializer
def roles_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [role.to_data(defaults = True) for role in value]
    return value


@ROLES_CONVERSION.set_value_validator
def roles_value_validator(value):
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
    ('communication_disabled_until',),
    'timed_out_until',
    value_validator = validate_timed_out_until,
)


@TIMED_OUT_UNTIL_CONVERSION.set_value_deserializer
def timed_out_until_converter_get(value):
    if (value is not None):
        value = timestamp_to_datetime(value)
    return value


@TIMED_OUT_UNTIL_CONVERSION.set_value_serializer
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
    ROLES_CONVERSION,
    TIMED_OUT_UNTIL_CONVERSION,
)
