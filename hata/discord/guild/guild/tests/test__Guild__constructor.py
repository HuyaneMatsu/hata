import vampytest

from scarletio import WeakValueDictionary
from ....bases import IconType
from ....localization import Locale
from ..guild import Guild
from ..preinstanced import ContentFilterLevel, MFA, NsfwLevel, VerificationLevel, MessageNotificationLevel, HubType
from ..flags import SystemChannelFlag


def _assert_fields_set(guild):
    """
    Asserts whether every fields of the guilds are set.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to check.
    """
    vampytest.assert_instance(guild, Guild)
    vampytest.assert_instance(guild._cache_boosters, tuple, nullable = True)
    vampytest.assert_instance(guild._cache_permission, dict, nullable = True)
    vampytest.assert_instance(guild._state, int)
    vampytest.assert_instance(guild.afk_channel_id, int)
    vampytest.assert_instance(guild.afk_timeout, int)
    vampytest.assert_instance(guild.approximate_online_count, int)
    vampytest.assert_instance(guild.approximate_user_count, int)
    vampytest.assert_instance(guild.available, bool)
    vampytest.assert_instance(guild.banner_hash, int)
    vampytest.assert_instance(guild.banner_type, IconType)
    vampytest.assert_instance(guild.boost_count, int)
    vampytest.assert_instance(guild.boost_progress_bar_enabled, bool)
    vampytest.assert_instance(guild.channels, dict)
    vampytest.assert_instance(guild.clients, list)
    vampytest.assert_instance(guild.content_filter, ContentFilterLevel)
    vampytest.assert_instance(guild.discovery_splash_hash, int)
    vampytest.assert_instance(guild.discovery_splash_type, IconType)
    vampytest.assert_instance(guild.description, str, nullable = True)
    vampytest.assert_instance(guild.embedded_activity_states, set, nullable = True)
    vampytest.assert_instance(guild.emojis, dict)
    vampytest.assert_instance(guild.features, tuple, nullable = True)
    vampytest.assert_instance(guild.hub_type, HubType)
    vampytest.assert_instance(guild.icon_hash, int)
    vampytest.assert_instance(guild.icon_type, IconType)
    vampytest.assert_instance(guild.id, int)
    vampytest.assert_instance(guild.invite_splash_hash, int)
    vampytest.assert_instance(guild.invite_splash_type, IconType)
    vampytest.assert_instance(guild.large, bool)
    vampytest.assert_instance(guild.max_presences, int)
    vampytest.assert_instance(guild.max_stage_channel_video_users, int)
    vampytest.assert_instance(guild.max_users, int)
    vampytest.assert_instance(guild.max_voice_channel_video_users, int)
    vampytest.assert_instance(guild.message_notification, MessageNotificationLevel)
    vampytest.assert_instance(guild.mfa, MFA)
    vampytest.assert_instance(guild.name, str)
    vampytest.assert_instance(guild.nsfw_level, NsfwLevel)
    vampytest.assert_instance(guild.owner_id, int)
    vampytest.assert_instance(guild.preferred_locale, Locale)
    vampytest.assert_instance(guild.premium_tier, int)
    vampytest.assert_instance(guild.public_updates_channel_id, int)
    vampytest.assert_instance(guild.safety_alerts_channel_id, int)
    vampytest.assert_instance(guild.roles, dict)
    vampytest.assert_instance(guild.rules_channel_id. int)
    vampytest.assert_instance(guild.scheduled_events, dict)
    vampytest.assert_instance(guild.soundboard_sounds, dict, nullable = True)
    vampytest.assert_instance(guild.stages, dict, nullable = True)
    vampytest.assert_instance(guild.stickers, dict)
    vampytest.assert_instance(guild.system_channel_id, int)
    vampytest.assert_instance(guild.system_channel_flags, SystemChannelFlag)
    vampytest.assert_instance(guild.threads, dict)
    vampytest.assert_instance(guild.user_count, int)
    vampytest.assert_instance(guild.users, dict, WeakValueDictionary)
    vampytest.assert_instance(guild.vanity_code, str, nullable = True)
    vampytest.assert_instance(guild.verification_level, VerificationLevel)
    vampytest.assert_instance(guild.voice_states, dict)
    vampytest.assert_instance(guild.widget_channel_id, int)
    vampytest.assert_instance(guild.widget_enabled, bool)
