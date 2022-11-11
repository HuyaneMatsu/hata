__all__ = ()

from ....channel import VoiceRegion
from ....localization import Locale

from ...flags import SystemChannelFlag
from ...preinstanced import ContentFilterLevel, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel


from ..audit_log_change import AuditLogChange

from .shared import (
    _convert_preinstanced, convert_deprecated, convert_icon, convert_nothing, convert_snowflake
)


def convert_content_filter(name, data):
    return _convert_preinstanced('content_filter', data, ContentFilterLevel)


def convert_hub_type(name, data):
    return _convert_preinstanced('hub_type', data, HubType)


def convert_bool__boost_progress_bar_enabled(name, data):
    return convert_nothing('boost_progress_bar_enabled', data)


def convert_int__days(name, data):
    return convert_nothing('days', data)


def convert_str__vanity_code(name, data):
    return convert_nothing('vanity_code', data)


def convert_message_notification(name, data):
    return _convert_preinstanced('message_notification', data, MessageNotificationLevel)


def convert_mfa(name, data):
    return _convert_preinstanced('mfa', data, MFA)


def convert_nsfw_level(name, data):
    return _convert_preinstanced('mfa', data, NsfwLevel)


def convert_voice_region(name, data):
    return _convert_preinstanced('region', data, VoiceRegion)


def convert_system_channel_flags(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = SystemChannelFlag(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = SystemChannelFlag(after)
    
    return AuditLogChange('system_channel_flags', before, after)


def convert_verification_level(name, data):
    return _convert_preinstanced('verification_level', data, VerificationLevel)


def convert_preferred_locale(name, data):
    return _convert_preinstanced('preferred_locale', data, Locale)


GUILD_CONVERTERS = {
    'afk_channel_id': convert_snowflake,
    'afk_timeout': convert_nothing,
    'application_id': convert_snowflake,
    'banner_hash': convert_icon,
    'default_message_notifications': convert_message_notification,
    'description': convert_nothing,
    'discovery_splash_hash': convert_icon,
    'explicit_content_filter': convert_content_filter,
    'hub_type': convert_hub_type,
    'icon_hash': convert_icon,
    'mfa_level': convert_mfa,
    'name': convert_nothing,
    'nsfw': convert_deprecated,
    'nsfw_level': convert_nsfw_level,
    'owner_id': convert_snowflake,
    'premium_progress_bar_enabled': convert_bool__boost_progress_bar_enabled,
    'preferred_locale': convert_preferred_locale,
    'prune_delete_days': convert_int__days,
    'public_updates_channel_id': convert_snowflake,
    'rules_channel_id': convert_snowflake,
    'region': convert_voice_region,
    'splash_hash': convert_icon,
    'system_channel_id': convert_snowflake,
    'system_channel_flags': convert_system_channel_flags,
    'vanity_url_code': convert_str__vanity_code,
    'verification_level': convert_verification_level,
    'widget_channel_id': convert_snowflake,
    'widget_enabled': convert_nothing,
}
