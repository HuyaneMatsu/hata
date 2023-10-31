__all__ = ()

from ...bases import Icon
from ...guild import (
    ContentFilterLevel, HubType, MFA, MessageNotificationLevel, NsfwLevel, SystemChannelFlag, VerificationLevel
)
from ...guild.guild.constants import (
    AFK_TIMEOUT_DEFAULT, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
)
from ...guild.guild.fields import (
    validate_afk_channel_id, validate_afk_timeout, validate_boost_progress_bar_enabled, validate_content_filter,
    validate_description, validate_hub_type, validate_locale, validate_max_stage_channel_video_users,
    validate_max_voice_channel_video_users, validate_message_notification, validate_mfa, validate_name,
    validate_nsfw_level, validate_owner_id, validate_public_updates_channel_id, validate_rules_channel_id,
    validate_safety_alerts_channel_id, validate_system_channel_flags, validate_system_channel_id, validate_vanity_code,
    validate_verification_level, validate_widget_channel_id, validate_widget_enabled
)
from ...guild.guild.guild import GUILD_BANNER, GUILD_DISCOVERY_SPLASH, GUILD_ICON, GUILD_INVITE_SPLASH
from ...localization import Locale

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_name, put_converter_description, put_converter_id,
    put_converter_name
)


# ---- afk_channel_id ----

AFK_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'afk_channel_id',
    'afk_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_afk_channel_id,
)


# ---- afk_timeout ----

AFK_TIMEOUT_CONVERSION = AuditLogEntryChangeConversion(
    'afk_timeout',
    'afk_timeout',
    FLAG_IS_MODIFICATION,
    validator = validate_afk_timeout,
)


@AFK_TIMEOUT_CONVERSION.set_get_converter
def afk_timeout_get_converter(value):
    if value is None:
        value = AFK_TIMEOUT_DEFAULT
    return value


# ---- banner ----

BANNER_CONVERSION = AuditLogEntryChangeConversion(
    'banner_hash',
    'banner',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = GUILD_BANNER.validate_icon,
)


# ---- boost_progress_bar_enabled ----

BOOST_PROGRESS_BAR_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    'premium_progress_bar_enabled',
    'boost_progress_bar_enabled',
    FLAG_IS_MODIFICATION,
    validator = validate_boost_progress_bar_enabled,
)


@BOOST_PROGRESS_BAR_ENABLED_CONVERSION.set_get_converter
def boost_progress_bar_enabled_get_converter(value):
    if value is None:
        value = False
    return value


# ---- content_filter ----

CONTENT_FILTER_CONVERSION = AuditLogEntryChangeConversion(
    'explicit_content_filter',
    'content_filter',
    FLAG_IS_MODIFICATION,
    validator = validate_content_filter,
)


@CONTENT_FILTER_CONVERSION.set_get_converter
def content_filter_get_converter(value):
    return ContentFilterLevel.get(value)


@CONTENT_FILTER_CONVERSION.set_put_converter
def content_filter_put_converter(value):
    return value.value


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    'description',
    'description',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_description,
)


# ---- discovery_splash ----

DISCOVERY_SPLASH_CONVERSION = AuditLogEntryChangeConversion(
    'discovery_splash_hash',
    'discovery_splash',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = GUILD_DISCOVERY_SPLASH.validate_icon,
)


# ---- hub_type ----

HUB_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'hub_type',
    'hub_type',
    FLAG_IS_MODIFICATION,
    validator = validate_hub_type,
)


@HUB_TYPE_CONVERSION.set_get_converter
def hub_type_get_converter(value):
    return HubType.get(value)


@HUB_TYPE_CONVERSION.set_put_converter
def hub_type_put_converter(value):
    return value.value


# ---- icon ----

ICON_CONVERSION = AuditLogEntryChangeConversion(
    'icon_hash',
    'icon',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = GUILD_ICON.validate_icon,
)


# ---- invite_splash ----

INVITE_SPLASH_CONVERSION = AuditLogEntryChangeConversion(
    'splash_hash',
    'invite_splash',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = GUILD_INVITE_SPLASH.validate_icon,
)


# ---- locale ----

LOCALE_CONVERSION = AuditLogEntryChangeConversion(
    'preferred_locale',
    'locale',
    FLAG_IS_MODIFICATION,
    validator = validate_locale,
)


@LOCALE_CONVERSION.set_get_converter
def locale_get_converter(value):
    return Locale.get(value)


@LOCALE_CONVERSION.set_put_converter
def locale_put_converter(value):
    return value.value


# ---- max_stage_channel_video_users ----

MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION = AuditLogEntryChangeConversion(
    'max_stage_video_channel_users',
    'max_stage_channel_video_users',
    FLAG_IS_MODIFICATION,
    validator = validate_max_stage_channel_video_users,
)


@MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.set_get_converter
def max_stage_channel_video_users_get_converter(value):
    if value is None:
        value = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
    return value


# ---- max_voice_channel_video_users ----

MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION = AuditLogEntryChangeConversion(
    'max_voice_video_channel_users',
    'max_voice_channel_video_users',
    FLAG_IS_MODIFICATION,
    validator = validate_max_voice_channel_video_users,
)


@MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.set_get_converter
def max_voice_channel_video_users_get_converter(value):
    if value is None:
        value = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
    return value


# ---- mfa ----

MFA_CONVERSION = AuditLogEntryChangeConversion(
    'mfa_level',
    'mfa',
    FLAG_IS_MODIFICATION,
    validator = validate_mfa,
)


@MFA_CONVERSION.set_get_converter
def mfa_get_converter(value):
    return MFA.get(value)


@MFA_CONVERSION.set_put_converter
def mfa_put_converter(value):
    return value.value


# ---- message_notification ----

MESSAGE_NOTIFICATION_CONVERSION = AuditLogEntryChangeConversion(
    'default_message_notifications',
    'message_notification',
    FLAG_IS_MODIFICATION,
    validator = validate_message_notification,
)


@MESSAGE_NOTIFICATION_CONVERSION.set_get_converter
def message_notification_get_converter(value):
    return MessageNotificationLevel.get(value)


@MESSAGE_NOTIFICATION_CONVERSION.set_put_converter
def message_notification_put_converter(value):
    return value.value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- nsfw_level ----

NSFW_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    'nsfw_level',
    'nsfw_level',
    FLAG_IS_MODIFICATION,
    validator = validate_nsfw_level,
)


@NSFW_LEVEL_CONVERSION.set_get_converter
def nsfw_level_get_converter(value):
    return NsfwLevel.get(value)


@NSFW_LEVEL_CONVERSION.set_put_converter
def nsfw_level_put_converter(value):
    return value.value


# ---- owner_id ----

OWNER_ID_CONVERSION = AuditLogEntryChangeConversion(
    'owner_id',
    'owner_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_owner_id,
)


# ---- public_updates_channel_id ----

PUBLIC_UPDATES_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'public_updates_channel_id',
    'public_updates_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_public_updates_channel_id,
)


# ---- rules_channel_id ----

RULES_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'rules_channel_id',
    'rules_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_rules_channel_id,
)


# ---- safety_alerts_channel_id ----

SAFETY_ALERTS_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'safety_alerts_channel_id',
    'safety_alerts_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_safety_alerts_channel_id,
)


# ---- system_channel_id ----

SYSTEM_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'system_channel_id',
    'system_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_system_channel_id,
)


# ---- system_channel_flags ----

SYSTEM_CHANNEL_FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    'system_channel_flags',
    'system_channel_flags',
    FLAG_IS_MODIFICATION,
    validator = validate_system_channel_flags,
)


@SYSTEM_CHANNEL_FLAGS_CONVERSION.set_get_converter
def system_channel_flags_get_converter(value):
    if value is None:
        value = SystemChannelFlag()
    else:
        value = SystemChannelFlag(value)
    
    return value


@SYSTEM_CHANNEL_FLAGS_CONVERSION.set_put_converter
def system_channel_flags_put_converter(value):
    return int(value)


# ---- vanity_code ----

VANITY_CODE_CONVERSION = AuditLogEntryChangeConversion(
    'vanity_url_code',
    'vanity_code',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_vanity_code,
)


# ---- verification_level ----

VERIFICATION_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    'verification_level',
    'verification_level',
    FLAG_IS_MODIFICATION,
    validator = validate_verification_level,
)


@VERIFICATION_LEVEL_CONVERSION.set_get_converter
def verification_level_get_converter(value):
    return VerificationLevel.get(value)


@VERIFICATION_LEVEL_CONVERSION.set_put_converter
def verification_level_put_converter(value):
    return value.value


# ---- widget_channel_id ----

WIDGET_CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'widget_channel_id',
    'widget_channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_widget_channel_id,
)


# ---- widget_enabled ----

WIDGET_ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    'widget_enabled',
    'widget_enabled',
    FLAG_IS_MODIFICATION,
    validator = validate_widget_enabled,
)


@WIDGET_ENABLED_CONVERSION.set_get_converter
def widget_enabled_get_converter(value):
    if value is None:
        value = False
    return value


# ---- Construct -----

GUILD_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AFK_CHANNEL_ID_CONVERSION,
    AFK_TIMEOUT_CONVERSION,
    BANNER_CONVERSION,
    BOOST_PROGRESS_BAR_ENABLED_CONVERSION,
    CONTENT_FILTER_CONVERSION,
    DESCRIPTION_CONVERSION,
    DISCOVERY_SPLASH_CONVERSION,
    HUB_TYPE_CONVERSION,
    ICON_CONVERSION,
    INVITE_SPLASH_CONVERSION,
    LOCALE_CONVERSION,
    MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION,
    MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION,
    MFA_CONVERSION,
    MESSAGE_NOTIFICATION_CONVERSION,
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
