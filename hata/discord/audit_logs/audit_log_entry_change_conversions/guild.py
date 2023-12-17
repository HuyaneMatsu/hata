__all__ = ()

from ...bases import Icon
from ...guild import (
    ExplicitContentFilterLevel, HubType, MfaLevel, MessageNotificationLevel, NsfwLevel, SystemChannelFlag,
    VerificationLevel
)
from ...guild.guild.constants import (
    AFK_TIMEOUT_DEFAULT, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
)
from ...guild.guild.fields import (
    validate_afk_channel_id, validate_afk_timeout, validate_boost_progress_bar_enabled,
    validate_default_message_notification_level, validate_description, validate_explicit_content_filter_level,
    validate_hub_type, validate_locale, validate_max_stage_channel_video_users, validate_max_voice_channel_video_users,
    validate_mfa_level, validate_name, validate_nsfw_level, validate_owner_id, validate_public_updates_channel_id,
    validate_rules_channel_id, validate_safety_alerts_channel_id, validate_system_channel_flags,
    validate_system_channel_id, validate_vanity_code, validate_verification_level, validate_widget_channel_id,
    validate_widget_enabled
)
from ...guild.guild.guild import GUILD_BANNER, GUILD_DISCOVERY_SPLASH, GUILD_ICON, GUILD_INVITE_SPLASH
from ...localization import Locale

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_name, value_serializer_description,
    value_serializer_id, value_serializer_name
)


# ---- afk_channel_id ----

AFK_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('afk_channel_id',),
    'afk_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_afk_channel_id,
)


# ---- afk_timeout ----

AFK_TIMEOUT_CONVERSION = AuditLogEntryChangeConversion(
    ('afk_timeout',),
    'afk_timeout',
    value_validator = validate_afk_timeout,
)


@AFK_TIMEOUT_CONVERSION.set_value_deserializer
def afk_timeout_value_deserializer(value):
    if value is None:
        value = AFK_TIMEOUT_DEFAULT
    return value


# ---- banner ----

BANNER_CONVERSION = AuditLogEntryChangeConversion(
    ('banner_hash',),
    'banner',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = GUILD_BANNER.validate_icon,
)


# ---- boost_progress_bar_enabled ----

BOOST_PROGRESS_BAR_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    ('premium_progress_bar_enabled',),
    'boost_progress_bar_enabled',
    value_validator = validate_boost_progress_bar_enabled,
)


@BOOST_PROGRESS_BAR_ENABLED_CONVERSION.set_value_deserializer
def boost_progress_bar_enabled_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    ('description',),
    'description',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_description,
)


# ---- discovery_splash ----

DISCOVERY_SPLASH_CONVERSION = AuditLogEntryChangeConversion(
    ('discovery_splash_hash',),
    'discovery_splash',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = GUILD_DISCOVERY_SPLASH.validate_icon,
)


# ---- content_filter ----

EXPLICIT_CONTENT_FILTER_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('explicit_content_filter',),
    'explicit_content_filter_level',
    value_validator = validate_explicit_content_filter_level,
)


@EXPLICIT_CONTENT_FILTER_LEVEL_CONVERSION.set_value_deserializer
def content_filter_value_deserializer(value):
    return ExplicitContentFilterLevel.get(value)


@EXPLICIT_CONTENT_FILTER_LEVEL_CONVERSION.set_value_serializer
def content_filter_value_serializer(value):
    return value.value


# ---- hub_type ----

HUB_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('hub_type',),
    'hub_type',
    value_validator = validate_hub_type,
)


@HUB_TYPE_CONVERSION.set_value_deserializer
def hub_type_value_deserializer(value):
    return HubType.get(value)


@HUB_TYPE_CONVERSION.set_value_serializer
def hub_type_value_serializer(value):
    return value.value


# ---- icon ----

ICON_CONVERSION = AuditLogEntryChangeConversion(
    ('icon_hash',),
    'icon',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = GUILD_ICON.validate_icon,
)


# ---- invite_splash ----

INVITE_SPLASH_CONVERSION = AuditLogEntryChangeConversion(
    ('splash_hash',),
    'invite_splash',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = GUILD_INVITE_SPLASH.validate_icon,
)


# ---- locale ----

LOCALE_CONVERSION = AuditLogEntryChangeConversion(
    ('preferred_locale',),
    'locale',
    value_validator = validate_locale,
)


@LOCALE_CONVERSION.set_value_deserializer
def locale_value_deserializer(value):
    return Locale.get(value)


@LOCALE_CONVERSION.set_value_serializer
def locale_value_serializer(value):
    return value.value


# ---- max_stage_channel_video_users ----

MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION = AuditLogEntryChangeConversion(
    ('max_stage_video_channel_users',),
    'max_stage_channel_video_users',
    value_validator = validate_max_stage_channel_video_users,
)


@MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.set_value_deserializer
def max_stage_channel_video_users_value_deserializer(value):
    if value is None:
        value = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
    return value


# ---- max_voice_channel_video_users ----

MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION = AuditLogEntryChangeConversion(
    ('max_voice_video_channel_users',),
    'max_voice_channel_video_users',
    value_validator = validate_max_voice_channel_video_users,
)


@MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.set_value_deserializer
def max_voice_channel_video_users_value_deserializer(value):
    if value is None:
        value = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
    return value


# ---- mfa_level ----

MFA_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('mfa_level',),
    'mfa_level',
    value_validator = validate_mfa_level,
)


@MFA_LEVEL_CONVERSION.set_value_deserializer
def mfa_level_value_deserializer(value):
    return MfaLevel.get(value)


@MFA_LEVEL_CONVERSION.set_value_serializer
def mfa_level_value_serializer(value):
    return value.value


# ---- message_notification ----

DEFAULT_MESSAGE_NOTIFICATION_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('default_message_notifications',),
    'default_message_notification_level',
    value_validator = validate_default_message_notification_level,
)


@DEFAULT_MESSAGE_NOTIFICATION_LEVEL_CONVERSION.set_value_deserializer
def message_notification_value_deserializer(value):
    return MessageNotificationLevel.get(value)


@DEFAULT_MESSAGE_NOTIFICATION_LEVEL_CONVERSION.set_value_serializer
def message_notification_value_serializer(value):
    return value.value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- nsfw_level ----

NSFW_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('nsfw_level',),
    'nsfw_level',
    value_validator = validate_nsfw_level,
)


@NSFW_LEVEL_CONVERSION.set_value_deserializer
def nsfw_level_value_deserializer(value):
    return NsfwLevel.get(value)


@NSFW_LEVEL_CONVERSION.set_value_serializer
def nsfw_level_value_serializer(value):
    return value.value


# ---- owner_id ----

OWNER_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('owner_id',),
    'owner_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_owner_id,
)


# ---- public_updates_channel_id ----

PUBLIC_UPDATES_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('public_updates_channel_id',),
    'public_updates_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_public_updates_channel_id,
)


# ---- rules_channel_id ----

RULES_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('rules_channel_id',),
    'rules_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_rules_channel_id,
)


# ---- safety_alerts_channel_id ----

SAFETY_ALERTS_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('safety_alerts_channel_id',),
    'safety_alerts_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_safety_alerts_channel_id,
)


# ---- system_channel_id ----

SYSTEM_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('system_channel_id',),
    'system_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_system_channel_id,
)


# ---- system_channel_flags ----

SYSTEM_CHANNEL_FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('system_channel_flags',),
    'system_channel_flags',
    value_validator = validate_system_channel_flags,
)


@SYSTEM_CHANNEL_FLAGS_CONVERSION.set_value_deserializer
def system_channel_flags_value_deserializer(value):
    if value is None:
        value = SystemChannelFlag()
    else:
        value = SystemChannelFlag(value)
    
    return value


@SYSTEM_CHANNEL_FLAGS_CONVERSION.set_value_serializer
def system_channel_flags_value_serializer(value):
    return int(value)


# ---- vanity_code ----

VANITY_CODE_CONVERSION = AuditLogEntryChangeConversion(
    ('vanity_url_code',),
    'vanity_code',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_vanity_code,
)


# ---- verification_level ----

VERIFICATION_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('verification_level',),
    'verification_level',
    value_validator = validate_verification_level,
)


@VERIFICATION_LEVEL_CONVERSION.set_value_deserializer
def verification_level_value_deserializer(value):
    return VerificationLevel.get(value)


@VERIFICATION_LEVEL_CONVERSION.set_value_serializer
def verification_level_value_serializer(value):
    return value.value


# ---- widget_channel_id ----

WIDGET_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('widget_channel_id',),
    'widget_channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_widget_channel_id,
)


# ---- widget_enabled ----

WIDGET_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    ('widget_enabled',),
    'widget_enabled',
    value_validator = validate_widget_enabled,
)


@WIDGET_ENABLED_CONVERSION.set_value_deserializer
def widget_enabled_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- Construct -----

GUILD_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AFK_CHANNEL_ID_CONVERSION,
    AFK_TIMEOUT_CONVERSION,
    BANNER_CONVERSION,
    BOOST_PROGRESS_BAR_ENABLED_CONVERSION,
    EXPLICIT_CONTENT_FILTER_LEVEL_CONVERSION,
    DESCRIPTION_CONVERSION,
    DISCOVERY_SPLASH_CONVERSION,
    HUB_TYPE_CONVERSION,
    ICON_CONVERSION,
    INVITE_SPLASH_CONVERSION,
    LOCALE_CONVERSION,
    MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION,
    MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION,
    MFA_LEVEL_CONVERSION,
    DEFAULT_MESSAGE_NOTIFICATION_LEVEL_CONVERSION,
    NAME_CONVERSION,
    NSFW_LEVEL_CONVERSION,
    OWNER_ID_CONVERSION,
    PUBLIC_UPDATES_CHANNEL_ID_CONVERSION,
    RULES_CHANNEL_ID_CONVERSION,
    SAFETY_ALERTS_CHANNEL_ID_CONVERSION,
    SYSTEM_CHANNEL_ID_CONVERSION,
    SYSTEM_CHANNEL_FLAGS_CONVERSION,
    VANITY_CODE_CONVERSION,
    VERIFICATION_LEVEL_CONVERSION,
    WIDGET_CHANNEL_ID_CONVERSION,
    WIDGET_ENABLED_CONVERSION,
)
