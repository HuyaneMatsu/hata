import vampytest
from scarletio import WeakValueDictionary

from ....activity import Activity
from ....bases import Icon, IconType
from ....channel import Channel, ChannelType
from ....emoji import Emoji
from ....localization import Locale
from ....role import Role
from ....scheduled_event import ScheduledEvent
from ....soundboard import SoundboardSound
from ....stage import Stage
from ....sticker import Sticker
from ....user import User, VoiceState

from ...embedded_activity_state import EmbeddedActivityState

from ..flags import SystemChannelFlag
from ..guild import Guild
from ..preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
)


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
    vampytest.assert_instance(guild.rules_channel_id, int)
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


def test__Guild__new__0():
    """
    Tests whether ``Guild.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild = Guild()
    _assert_fields_set(guild)


def test__Guild__new__1():
    """
    Tests whether ``Guild.__new__`` works as intended.
    
    Case: All fields given.
    """
    afk_channel_id = 202306210000
    afk_timeout = 1800
    banner = Icon(IconType.animated, 12)
    boost_progress_bar_enabled = True
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    message_notification = MessageNotificationLevel.no_messages
    mfa = MFA.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306210001
    preferred_locale = Locale.finnish
    public_updates_channel_id = 202306210002
    rules_channel_id = 202306210004
    safety_alerts_channel_id = 202306210003
    system_channel_id = 202306210005
    system_channel_flags = SystemChannelFlag(12)
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    widget_channel_id = 202306210006
    widget_enabled = True
    
    guild = Guild(
        afk_channel_id = afk_channel_id,
        afk_timeout = afk_timeout,
        banner = banner,
        boost_progress_bar_enabled = boost_progress_bar_enabled,
        content_filter = content_filter,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        hub_type = hub_type,
        icon = icon,
        invite_splash = invite_splash,
        message_notification = message_notification,
        mfa = mfa,
        name = name,
        nsfw_level = nsfw_level,
        owner_id = owner_id,
        preferred_locale = preferred_locale,
        public_updates_channel_id = public_updates_channel_id,
        rules_channel_id = rules_channel_id,
        safety_alerts_channel_id = safety_alerts_channel_id,
        system_channel_id = system_channel_id,
        system_channel_flags = system_channel_flags,
        vanity_code = vanity_code,
        verification_level = verification_level,
        widget_channel_id = widget_channel_id,
        widget_enabled = widget_enabled,
    )
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.afk_channel_id, afk_channel_id)
    vampytest.assert_eq(guild.afk_timeout, afk_timeout)
    vampytest.assert_eq(guild.banner, banner)
    vampytest.assert_eq(guild.boost_progress_bar_enabled, boost_progress_bar_enabled)
    vampytest.assert_is(guild.content_filter, content_filter)
    vampytest.assert_eq(guild.description, description)
    vampytest.assert_eq(guild.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild.features, tuple(features))
    vampytest.assert_is(guild.hub_type, hub_type)
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.invite_splash, invite_splash)
    vampytest.assert_is(guild.message_notification, message_notification)
    vampytest.assert_is(guild.mfa, mfa)
    vampytest.assert_eq(guild.name, name)
    vampytest.assert_is(guild.nsfw_level, nsfw_level)
    vampytest.assert_eq(guild.owner_id, owner_id)
    vampytest.assert_is(guild.preferred_locale, preferred_locale)
    vampytest.assert_eq(guild.public_updates_channel_id, public_updates_channel_id)
    vampytest.assert_eq(guild.rules_channel_id, rules_channel_id)
    vampytest.assert_eq(guild.safety_alerts_channel_id, safety_alerts_channel_id)
    vampytest.assert_eq(guild.system_channel_id, system_channel_id)
    vampytest.assert_eq(guild.system_channel_flags, system_channel_flags)
    vampytest.assert_eq(guild.vanity_code, vanity_code)
    vampytest.assert_eq(guild.verification_level, verification_level)
    vampytest.assert_eq(guild.widget_channel_id, widget_channel_id)
    vampytest.assert_eq(guild.widget_enabled, widget_enabled)


def test__Guild__create_empty():
    """
    Tests whether ``Guild._create_empty`` works as intended.
    """
    guild_id = 202306210007
    
    guild = Guild._create_empty(guild_id)
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)


def test__Guild__precreate__0():
    """
    Tests whether ``Guild.precreate`` works as intended.
    
    Case: No fields given.
    """
    guild_id = 202306210008
    
    guild = Guild.precreate(guild_id)
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)


def test__Guild__precreate__1():
    """
    Tests whether ``Guild.precreate`` works as intended.
    
    Case: Caching.
    """
    guild_id = 202306210009
    
    guild_0 = Guild.precreate(guild_id)
    guild_1 = Guild.precreate(guild_id)
    
    vampytest.assert_is(guild_0, guild_1)


def test__Guild__precreate__2():
    """
    Tests whether ``Guild.precreate`` works as intended.
    
    Case: All fields given.
    """
    guild_id = 202306210010
    
    afk_channel_id = 202306210011
    afk_timeout = 1800
    approximate_online_count = 69
    approximate_user_count = 70
    available = True
    banner = Icon(IconType.animated, 12)
    boost_count = 3
    boost_progress_bar_enabled = True
    channels = [
        Channel.precreate(202306210012, channel_type = ChannelType.guild_text),
        Channel.precreate(202306210013, channel_type = ChannelType.guild_voice),
    ]
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    embedded_activity_states = [
        EmbeddedActivityState(activity = Activity('dance'), guild_id = guild_id, channel_id = 202306220034),
        EmbeddedActivityState(activity = Activity('party'), guild_id = guild_id, channel_id = 202306220035),
    ]
    emojis = [
        Emoji.precreate(202306210014),
        Emoji.precreate(202306210015),
    ]
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    large = True
    max_presences = 420
    max_stage_channel_video_users = 421
    max_users = 422
    max_voice_channel_video_users = 423
    message_notification = MessageNotificationLevel.no_messages
    mfa = MFA.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306210016
    preferred_locale = Locale.finnish
    premium_tier = 1
    public_updates_channel_id = 202306210017
    roles = [
        Role.precreate(202306210019),
        Role.precreate(202306210020),
    ]
    rules_channel_id = 202306210021
    scheduled_events = [
        ScheduledEvent.precreate(202306210022),
        ScheduledEvent.precreate(202306210023),
    ]
    safety_alerts_channel_id = 202306210018
    soundboard_sounds = [
        SoundboardSound.precreate(202306210024),
        SoundboardSound.precreate(202306210025),
    ]
    stages = [
        Stage.precreate(202306210026),
        Stage.precreate(202306210027),
    ]
    stickers = [
        Sticker.precreate(202306210028),
        Sticker.precreate(202306210029),
    ]
    system_channel_id = 202306210030
    system_channel_flags = SystemChannelFlag(12)
    threads = [
        Channel.precreate(202306210031, channel_type = ChannelType.guild_thread_private),
        Channel.precreate(202306210032, channel_type = ChannelType.guild_thread_public),
    ]
    user_count = 2
    users = [
        User.precreate(202306210033),
        User.precreate(202306210034),
    ]
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    voice_states = [
        VoiceState(guild_id = guild_id, user_id = 202306210035),
        VoiceState(guild_id = guild_id, user_id = 202306210036),
    ]
    widget_channel_id = 202306210037
    widget_enabled = True
    
    guild = Guild.precreate(
        guild_id,
        afk_channel_id = afk_channel_id,
        afk_timeout = afk_timeout,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        available = available,
        banner = banner,
        boost_count = boost_count,
        boost_progress_bar_enabled = boost_progress_bar_enabled,
        channels = channels,
        content_filter = content_filter,
        description = description,
        discovery_splash = discovery_splash,
        embedded_activity_states = embedded_activity_states,
        emojis = emojis,
        features = features,
        hub_type = hub_type,
        icon = icon,
        invite_splash = invite_splash,
        large = large,
        max_presences = max_presences,
        max_stage_channel_video_users = max_stage_channel_video_users,
        max_users = max_users,
        max_voice_channel_video_users = max_voice_channel_video_users,
        message_notification = message_notification,
        mfa = mfa,
        name = name,
        nsfw_level = nsfw_level,
        owner_id = owner_id,
        preferred_locale = preferred_locale,
        premium_tier = premium_tier,
        public_updates_channel_id = public_updates_channel_id,
        roles = roles,
        rules_channel_id = rules_channel_id,
        safety_alerts_channel_id = safety_alerts_channel_id,
        soundboard_sounds = soundboard_sounds,
        scheduled_events = scheduled_events,
        stages = stages,
        stickers = stickers,
        system_channel_id = system_channel_id,
        system_channel_flags = system_channel_flags,
        threads = threads,
        user_count = user_count,
        users = users,
        vanity_code = vanity_code,
        verification_level = verification_level,
        voice_states = voice_states,
        widget_channel_id = widget_channel_id,
        widget_enabled = widget_enabled,
    )
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.afk_channel_id, afk_channel_id)
    vampytest.assert_eq(guild.afk_timeout, afk_timeout)
    vampytest.assert_eq(guild.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, approximate_user_count)
    vampytest.assert_eq(guild.available, available)
    vampytest.assert_eq(guild.banner, banner)
    vampytest.assert_eq(guild.boost_count, boost_count)
    vampytest.assert_eq(guild.boost_progress_bar_enabled, boost_progress_bar_enabled)
    vampytest.assert_eq(guild.channels, {channel.id: channel for channel in channels})
    vampytest.assert_is(guild.content_filter, content_filter)
    vampytest.assert_eq(guild.description, description)
    vampytest.assert_eq(guild.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild.embedded_activity_states, set(embedded_activity_states))
    vampytest.assert_eq(guild.emojis, {emoji.id: emoji for emoji in emojis})
    vampytest.assert_eq(guild.features, tuple(features))
    vampytest.assert_is(guild.hub_type, hub_type)
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.invite_splash, invite_splash)
    vampytest.assert_eq(guild.large, large)
    vampytest.assert_eq(guild.max_presences, max_presences)
    vampytest.assert_eq(guild.max_stage_channel_video_users, max_stage_channel_video_users)
    vampytest.assert_eq(guild.max_users, max_users)
    vampytest.assert_eq(guild.max_voice_channel_video_users, max_voice_channel_video_users)
    vampytest.assert_is(guild.message_notification, message_notification)
    vampytest.assert_is(guild.mfa, mfa)
    vampytest.assert_eq(guild.name, name)
    vampytest.assert_is(guild.nsfw_level, nsfw_level)
    vampytest.assert_eq(guild.owner_id, owner_id)
    vampytest.assert_is(guild.preferred_locale, preferred_locale)
    vampytest.assert_eq(guild.premium_tier, premium_tier)
    vampytest.assert_eq(guild.public_updates_channel_id, public_updates_channel_id)
    vampytest.assert_eq(guild.roles, {role.id: role for role in roles})
    vampytest.assert_eq(guild.rules_channel_id, rules_channel_id)
    vampytest.assert_eq(guild.safety_alerts_channel_id, safety_alerts_channel_id)
    vampytest.assert_eq(
        guild.scheduled_events, {scheduled_event.id: scheduled_event for scheduled_event in scheduled_events}
    )
    vampytest.assert_eq(
        guild.soundboard_sounds, {soundboard_sound.id: soundboard_sound for soundboard_sound in soundboard_sounds}
    )
    vampytest.assert_eq(guild.stages, {stage.id: stage for stage in stages})
    vampytest.assert_eq(guild.stickers, {sticker.id: sticker for sticker in stickers})
    vampytest.assert_eq(guild.system_channel_id, system_channel_id)
    vampytest.assert_eq(guild.system_channel_flags, system_channel_flags)
    vampytest.assert_eq(guild.threads, {thread.id: thread for thread in threads})
    vampytest.assert_eq(guild.user_count, user_count)
    vampytest.assert_eq(guild.users, {user.id: user for user in users})
    vampytest.assert_eq(guild.vanity_code, vanity_code)
    vampytest.assert_eq(guild.verification_level, verification_level)
    vampytest.assert_eq(guild.voice_states, {voice_state.user_id: voice_state for voice_state in voice_states})
    vampytest.assert_eq(guild.widget_channel_id, widget_channel_id)
    vampytest.assert_eq(guild.widget_enabled, widget_enabled)
