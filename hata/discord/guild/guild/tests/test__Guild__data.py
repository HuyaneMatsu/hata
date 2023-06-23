import vampytest

from ....activity import Activity
from ....bases import Icon, IconType
from ....channel import Channel, ChannelType
from ....client import Client
from ....emoji import Emoji
from ....localization import Locale
from ....role import Role
from ....scheduled_event import ScheduledEvent
from ....soundboard import SoundboardSound
from ....stage import Stage
from ....sticker import Sticker
from ....user import GuildProfile, User, VoiceState

from ...embedded_activity_state import EmbeddedActivityState

from ..flags import SystemChannelFlag
from ..guild import Guild
from ..preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
)

from .test__Guild__constructor import _assert_fields_set



def test__Guild__from_data__0():
    """
    Tests whether ``Guild.from_data`` works as intended.
    
    Case: No fields given.
    """
    guild_id = 202306210065
    
    data = {
        'id': str(guild_id),
    }
    
    guild = Guild.from_data(data)
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)


def test__Guild__from_data__1():
    """
    Tests whether ``Guild.from_data`` works as intended.
    
    Case: All fields given.
    """
    guild_id = 202306210038
    
    afk_channel_id = 202306210039
    afk_timeout = 1800
    approximate_online_count = 69
    approximate_user_count = 70
    available = True
    banner = Icon(IconType.animated, 12)
    boost_count = 3
    boost_progress_bar_enabled = True
    channels = [
        Channel.precreate(202306210040, channel_type = ChannelType.guild_text),
        Channel.precreate(202306210041, channel_type = ChannelType.guild_voice),
    ]
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    embedded_activity_states = [
        EmbeddedActivityState(activity = Activity('dance'), guild_id = guild_id, channel_id = 202306220032),
        EmbeddedActivityState(activity = Activity('party'), guild_id = guild_id, channel_id = 202306220033),
    ]
    emojis = [
        Emoji.precreate(202306210042),
        Emoji.precreate(202306210043),
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
    owner_id = 202306210044
    preferred_locale = Locale.finnish
    premium_tier = 1
    public_updates_channel_id = 202306210045
    roles = [
        Role.precreate(202306210046),
        Role.precreate(202306210047),
    ]
    rules_channel_id = 202306210048
    scheduled_events = [
        ScheduledEvent.precreate(202306210049),
        ScheduledEvent.precreate(202306210050),
    ]
    safety_alerts_channel_id = 202306210051
    # soundboard_sounds = [SoundboardSound.precreate(202306210052), SoundboardSound.precreate(202306210053),]
    stages = [
        Stage.precreate(202306210054),
        Stage.precreate(202306210055),
    ]
    stickers = [
        Sticker.precreate(202306210056),
        Sticker.precreate(202306210057),
    ]
    system_channel_id = 202306210030
    system_channel_flags = SystemChannelFlag(12)
    threads = [
        Channel.precreate(202306210058, channel_type = ChannelType.guild_thread_private),
        Channel.precreate(202306210059, channel_type = ChannelType.guild_thread_public),
    ]
    user_count = 2
    users = [
        User.precreate(202306210060),
        User.precreate(202306210061),
    ]
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    voice_states = [
        VoiceState(guild_id = guild_id, user_id = 202306210062, channel_id = 202306210066),
        VoiceState(guild_id = guild_id, user_id = 202306210063, channel_id = 202306210067),
    ]
    widget_channel_id = 202306210064
    widget_enabled = True
    
    
    data = {
        'id': str(guild_id),
        'afk_channel_id': str(afk_channel_id),
        'afk_timeout': afk_timeout,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'unavailable': not available,
        'premium_progress_bar_enabled': boost_progress_bar_enabled,
        'premium_subscription_count': boost_count,
        'channels': [channel.to_data(include_internals = True) for channel in channels],
        'explicit_content_filter': content_filter.value,
        'description': description,
        'embedded_activities': [
            embedded_activity_state.to_data() for embedded_activity_state in embedded_activity_states
        ],
        'emojis': [emoji.to_data(include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'hub_type': hub_type.value,
        'large': large,
        'max_presences': max_presences,
        'max_stage_video_channel_users': max_stage_channel_video_users,
        'max_members': max_users,
        'max_video_channel_users': max_voice_channel_video_users,
        'default_message_notifications': message_notification.value,
        'mfa_level': mfa.value,
        'name': name,
        'nsfw_level': nsfw_level.value,
        'owner_id': str(owner_id),
        'preferred_locale': preferred_locale.value,
        'premium_tier': premium_tier,
        'public_updates_channel_id': str(public_updates_channel_id),
        'roles': [role.to_data(include_internals = True) for role in roles],
        'rules_channel_id': str(rules_channel_id),
        'safety_alerts_channel_id': str(safety_alerts_channel_id),
        # soundboard_sounds: [soundboard_sound.to_data(include_internals = True) for soundboard_sound in soundboard_sounds],
        'guild_scheduled_events': [
            scheduled_event.to_data(include_internals = True) for scheduled_event in scheduled_events
        ],
        'stage_instances': [stage.to_data(include_internals = True) for stage in stages],
        'stickers': [sticker.to_data(include_internals = True) for sticker in stickers],
        'system_channel_flags': int(system_channel_flags),
        'system_channel_id': str(system_channel_id),
        'threads': [channel.to_data(include_internals = True) for channel in threads],
        'member_count': user_count,
        'members': [
            {**GuildProfile().to_data(include_internals = True), 'user': user.to_data(include_internals = True)}
            for user in users
        ],
        'vanity_url_code': vanity_code,
        'verification_level': verification_level.value,
        'voice_states': [voice_state.to_data() for voice_state in voice_states],
        'widget_channel_id': str(widget_channel_id),
        'widget_enabled': widget_enabled,
        'icon': icon.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
    }
    
    guild = Guild.from_data(data)
    
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
    # vampytest.assert_eq(guild.soundboard_sounds, {soundboard_sound.id: soundboard_sound for soundboard_sound in soundboard_sounds})
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


def test__Guild__from_data__2():
    """
    Tests whether ``Guild.from_data`` works as intended.
    
    Case: Caching.
    """
    guild_id = 202306210068
    
    data = {
        'id': str(guild_id),
    }
    
    guild_0 = Guild.from_data(data)
    guild_1 = Guild.from_data(data)
    
    vampytest.assert_is(guild_0, guild_1)


def test__Guild__from_data__3():
    """
    Tests whether ``Guild.from_data`` works as intended.
    
    Case: strong caching.
    """
    guild_id = 202306210069
    
    data = {
        'id': str(guild_id),
    }
    
    client = Client(
        token = 'token_20230621_0000',
    )
    
    try:
        guild = Guild.from_data(data, client)
        
        vampytest.assert_eq(guild.clients, [client])
        vampytest.assert_eq(client.guilds, {guild})
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Guild__to_data():
    """
    Tests whether ``Guild.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    guild_id = 202306220000
    
    afk_channel_id = 202306220001
    afk_timeout = 1800
    approximate_online_count = 69
    approximate_user_count = 70
    available = True
    banner = Icon(IconType.animated, 12)
    boost_count = 3
    boost_progress_bar_enabled = True
    channels = [
        Channel.precreate(202306220002, channel_type = ChannelType.guild_text),
        Channel.precreate(202306220003, channel_type = ChannelType.guild_voice),
    ]
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    embedded_activity_states = [
        EmbeddedActivityState(activity = Activity('dance'), guild_id = guild_id, channel_id = 202306220030),
        EmbeddedActivityState(activity = Activity('party'), guild_id = guild_id, channel_id = 202306220031),
    ]
    emojis = [
        Emoji.precreate(202306220004),
        Emoji.precreate(202306220005),
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
    owner_id = 202306220006
    preferred_locale = Locale.finnish
    premium_tier = 1
    public_updates_channel_id = 202306220007
    roles = [
        Role.precreate(202306220008),
        Role.precreate(202306220009),
    ]
    rules_channel_id = 202306220010
    scheduled_events = [
        ScheduledEvent.precreate(202306220011),
        ScheduledEvent.precreate(202306220012),
    ]
    safety_alerts_channel_id = 202306220013
    # soundboard_sounds = [SoundboardSound.precreate(202306220014), SoundboardSound.precreate(202306220015),]
    stages = [
        Stage.precreate(202306220016),
        Stage.precreate(202306220017),
    ]
    stickers = [
        Sticker.precreate(202306220018),
        Sticker.precreate(202306220019),
    ]
    system_channel_id = 202306220020
    system_channel_flags = SystemChannelFlag(12)
    threads = [
        Channel.precreate(202306220021, channel_type = ChannelType.guild_thread_private),
        Channel.precreate(202306220022, channel_type = ChannelType.guild_thread_public),
    ]
    user_count = 2
    users = [
        User.precreate(202306220023),
        User.precreate(202306220024),
    ]
    for user in users:
        user.guild_profiles[guild_id] = GuildProfile()
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    voice_states = [
        VoiceState(guild_id = guild_id, user_id = 202306220025, channel_id = 202306220026),
        VoiceState(guild_id = guild_id, user_id = 202306220027, channel_id = 202306220028),
    ]
    widget_channel_id = 202306220029
    widget_enabled = True
    

    expected_output = {
        'id': str(guild_id),
        'afk_channel_id': str(afk_channel_id),
        'afk_timeout': afk_timeout,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'unavailable': not available,
        'premium_progress_bar_enabled': boost_progress_bar_enabled,
        'premium_subscription_count': boost_count,
        'channels': [channel.to_data(defaults = True, include_internals = True) for channel in channels],
        'explicit_content_filter': content_filter.value,
        'description': description,
        'embedded_activities': [
            embedded_activity_state.to_data(defaults = True) for embedded_activity_state in embedded_activity_states
        ],
        'emojis': [emoji.to_data(defaults = True, include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'hub_type': hub_type.value,
        'large': large,
        'max_presences': max_presences,
        'max_stage_video_channel_users': max_stage_channel_video_users,
        'max_members': max_users,
        'max_video_channel_users': max_voice_channel_video_users,
        'default_message_notifications': message_notification.value,
        'mfa_level': mfa.value,
        'name': name,
        'nsfw_level': nsfw_level.value,
        'owner_id': str(owner_id),
        'preferred_locale': preferred_locale.value,
        'premium_tier': premium_tier,
        'public_updates_channel_id': str(public_updates_channel_id),
        'roles': [role.to_data(defaults = True, include_internals = True) for role in roles],
        'rules_channel_id': str(rules_channel_id),
        'safety_alerts_channel_id': str(safety_alerts_channel_id),
        # soundboard_sounds: [soundboard_sound.to_data(defaults = True, include_internals = True) for soundboard_sound in soundboard_sounds],
        'guild_scheduled_events': [
            scheduled_event.to_data(defaults = True, include_internals = True) for scheduled_event in scheduled_events
        ],
        'stage_instances': [stage.to_data(defaults = True, include_internals = True) for stage in stages],
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
        'system_channel_flags': int(system_channel_flags),
        'system_channel_id': str(system_channel_id),
        'threads': [channel.to_data(defaults = True, include_internals = True) for channel in threads],
        'member_count': user_count,
        'members': [
            {
                **GuildProfile().to_data(defaults = True, include_internals = True),
                'user': user.to_data(defaults = True, include_internals = True)
            } for user in users
        ],
        'vanity_url_code': vanity_code,
        'verification_level': verification_level.value,
        'voice_states': [voice_state.to_data(defaults = True) for voice_state in voice_states],
        'widget_channel_id': str(widget_channel_id),
        'widget_enabled': widget_enabled,
        'icon': icon.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
    }
    
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
        # soundboard_sounds = soundboard_sounds,
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
    
    vampytest.assert_eq(
        guild.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Guild__set_attributes__create():
    """
    Tests whether ``Guild._set_attributes`` works as intended.
    
    Case: New guild.
    """
    guild_id = 202306220036
    
    afk_channel_id = 202306220037
    afk_timeout = 1800
    approximate_online_count = 69
    approximate_user_count = 70
    available = True
    banner = Icon(IconType.animated, 12)
    boost_count = 3
    boost_progress_bar_enabled = True
    channels = [
        Channel.precreate(202306220038, channel_type = ChannelType.guild_text),
        Channel.precreate(202306220039, channel_type = ChannelType.guild_voice),
    ]
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    embedded_activity_states = [
        EmbeddedActivityState(activity = Activity('dance'), guild_id = guild_id, channel_id = 202306220040),
        EmbeddedActivityState(activity = Activity('party'), guild_id = guild_id, channel_id = 202306220041),
    ]
    emojis = [
        Emoji.precreate(202306220042),
        Emoji.precreate(202306220043),
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
    owner_id = 202306220044
    preferred_locale = Locale.finnish
    premium_tier = 1
    public_updates_channel_id = 202306220045
    roles = [
        Role.precreate(202306220046),
        Role.precreate(202306220047),
    ]
    rules_channel_id = 202306220048
    scheduled_events = [
        ScheduledEvent.precreate(202306220049),
        ScheduledEvent.precreate(202306220050),
    ]
    safety_alerts_channel_id = 202306220051
    # soundboard_sounds = [SoundboardSound.precreate(202306220052), SoundboardSound.precreate(202306220053),]
    stages = [
        Stage.precreate(202306220054),
        Stage.precreate(202306220055),
    ]
    stickers = [
        Sticker.precreate(202306220056),
        Sticker.precreate(202306220057),
    ]
    system_channel_id = 202306220058
    system_channel_flags = SystemChannelFlag(12)
    threads = [
        Channel.precreate(202306220059, channel_type = ChannelType.guild_thread_private),
        Channel.precreate(202306220060, channel_type = ChannelType.guild_thread_public),
    ]
    user_count = 2
    users = [
        User.precreate(202306220061),
        User.precreate(202306220062),
    ]
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    voice_states = [
        VoiceState(guild_id = guild_id, user_id = 202306220063, channel_id = 202306220064),
        VoiceState(guild_id = guild_id, user_id = 202306220065, channel_id = 202306220066),
    ]
    widget_channel_id = 202306220067
    widget_enabled = True
    
    
    data = {
        'id': str(guild_id),
        'afk_channel_id': str(afk_channel_id),
        'afk_timeout': afk_timeout,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'unavailable': not available,
        'premium_progress_bar_enabled': boost_progress_bar_enabled,
        'premium_subscription_count': boost_count,
        'channels': [channel.to_data(include_internals = True) for channel in channels],
        'explicit_content_filter': content_filter.value,
        'description': description,
        'embedded_activities': [
            embedded_activity_state.to_data() for embedded_activity_state in embedded_activity_states
        ],
        'emojis': [emoji.to_data(include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'hub_type': hub_type.value,
        'large': large,
        'max_presences': max_presences,
        'max_stage_video_channel_users': max_stage_channel_video_users,
        'max_members': max_users,
        'max_video_channel_users': max_voice_channel_video_users,
        'default_message_notifications': message_notification.value,
        'mfa_level': mfa.value,
        'name': name,
        'nsfw_level': nsfw_level.value,
        'owner_id': str(owner_id),
        'preferred_locale': preferred_locale.value,
        'premium_tier': premium_tier,
        'public_updates_channel_id': str(public_updates_channel_id),
        'roles': [role.to_data(include_internals = True) for role in roles],
        'rules_channel_id': str(rules_channel_id),
        'safety_alerts_channel_id': str(safety_alerts_channel_id),
        # soundboard_sounds: [soundboard_sound.to_data(include_internals = True) for soundboard_sound in soundboard_sounds],
        'guild_scheduled_events': [
            scheduled_event.to_data(include_internals = True) for scheduled_event in scheduled_events
        ],
        'stage_instances': [stage.to_data(include_internals = True) for stage in stages],
        'stickers': [sticker.to_data(include_internals = True) for sticker in stickers],
        'system_channel_flags': int(system_channel_flags),
        'system_channel_id': str(system_channel_id),
        'threads': [channel.to_data(include_internals = True) for channel in threads],
        'member_count': user_count,
        'members': [
            {**GuildProfile().to_data(include_internals = True), 'user': user.to_data(include_internals = True)}
            for user in users
        ],
        'vanity_url_code': vanity_code,
        'verification_level': verification_level.value,
        'voice_states': [voice_state.to_data() for voice_state in voice_states],
        'widget_channel_id': str(widget_channel_id),
        'widget_enabled': widget_enabled,
        'icon': icon.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
    }
    
    guild = object.__new__(Guild)
    guild.id = guild_id
    guild._set_attributes(data, True)
    
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
    # vampytest.assert_eq(guild.soundboard_sounds, {soundboard_sound.id: soundboard_sound for soundboard_sound in soundboard_sounds})
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


def test__Guild__set_attributes__existing():
    """
    Tests whether ``Guild._set_attributes`` works as intended.
    
    Case: existing guild.
    """
    guild_id = 202306220068
    
    afk_channel_id = 202306220069
    afk_timeout = 1800
    approximate_online_count = 69
    approximate_user_count = 70
    available = True
    banner = Icon(IconType.animated, 12)
    boost_count = 3
    boost_progress_bar_enabled = True
    channels = [
        Channel.precreate(202306220070, channel_type = ChannelType.guild_text),
        Channel.precreate(202306220071, channel_type = ChannelType.guild_voice),
    ]
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    embedded_activity_states = [
        EmbeddedActivityState(activity = Activity('dance'), guild_id = guild_id, channel_id = 202306220072),
        EmbeddedActivityState(activity = Activity('party'), guild_id = guild_id, channel_id = 202306220073),
    ]
    emojis = [
        Emoji.precreate(202306220074),
        Emoji.precreate(202306220075),
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
    owner_id = 202306220044
    preferred_locale = Locale.finnish
    premium_tier = 1
    public_updates_channel_id = 202306220076
    roles = [
        Role.precreate(202306220077),
        Role.precreate(202306220078),
    ]
    rules_channel_id = 202306220079
    scheduled_events = [
        ScheduledEvent.precreate(202306220080),
        ScheduledEvent.precreate(202306220081),
    ]
    safety_alerts_channel_id = 202306220082
    # soundboard_sounds = [SoundboardSound.precreate(202306220083), SoundboardSound.precreate(202306220084),]
    stages = [
        Stage.precreate(202306220085),
        Stage.precreate(202306220086),
    ]
    stickers = [
        Sticker.precreate(202306220087),
        Sticker.precreate(202306220088),
    ]
    system_channel_id = 202306220089
    system_channel_flags = SystemChannelFlag(12)
    threads = [
        Channel.precreate(202306220090, channel_type = ChannelType.guild_thread_private),
        Channel.precreate(202306220091, channel_type = ChannelType.guild_thread_public),
    ]
    user_count = 2
    users = [
        User.precreate(202306220092),
        User.precreate(202306220093),
    ]
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    voice_states = [
        VoiceState(guild_id = guild_id, user_id = 202306220094, channel_id = 202306220095),
        VoiceState(guild_id = guild_id, user_id = 202306220096, channel_id = 202306220097),
    ]
    widget_channel_id = 202306220098
    widget_enabled = True
    
    
    data = {
        'id': str(guild_id),
        'afk_channel_id': str(afk_channel_id),
        'afk_timeout': afk_timeout,
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'unavailable': not available,
        'premium_progress_bar_enabled': boost_progress_bar_enabled,
        'premium_subscription_count': boost_count,
        'channels': [channel.to_data(include_internals = True) for channel in channels],
        'explicit_content_filter': content_filter.value,
        'description': description,
        'embedded_activities': [
            embedded_activity_state.to_data() for embedded_activity_state in embedded_activity_states
        ],
        'emojis': [emoji.to_data(include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'hub_type': hub_type.value,
        'large': large,
        'max_presences': max_presences,
        'max_stage_video_channel_users': max_stage_channel_video_users,
        'max_members': max_users,
        'max_video_channel_users': max_voice_channel_video_users,
        'default_message_notifications': message_notification.value,
        'mfa_level': mfa.value,
        'name': name,
        'nsfw_level': nsfw_level.value,
        'owner_id': str(owner_id),
        'preferred_locale': preferred_locale.value,
        'premium_tier': premium_tier,
        'public_updates_channel_id': str(public_updates_channel_id),
        'roles': [role.to_data(include_internals = True) for role in roles],
        'rules_channel_id': str(rules_channel_id),
        'safety_alerts_channel_id': str(safety_alerts_channel_id),
        # soundboard_sounds: [soundboard_sound.to_data(include_internals = True) for soundboard_sound in soundboard_sounds],
        'guild_scheduled_events': [
            scheduled_event.to_data(include_internals = True) for scheduled_event in scheduled_events
        ],
        'stage_instances': [stage.to_data(include_internals = True) for stage in stages],
        'stickers': [sticker.to_data(include_internals = True) for sticker in stickers],
        'system_channel_flags': int(system_channel_flags),
        'system_channel_id': str(system_channel_id),
        'threads': [channel.to_data(include_internals = True) for channel in threads],
        'member_count': user_count,
        'members': [
            {**GuildProfile().to_data(include_internals = True), 'user': user.to_data(include_internals = True)}
            for user in users
        ],
        'vanity_url_code': vanity_code,
        'verification_level': verification_level.value,
        'voice_states': [voice_state.to_data() for voice_state in voice_states],
        'widget_channel_id': str(widget_channel_id),
        'widget_enabled': widget_enabled,
        'icon': icon.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
    }
    
    guild = Guild._create_empty(guild_id)
    guild._set_attributes(data, False)
    
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
    # vampytest.assert_eq(guild.soundboard_sounds, {soundboard_sound.id: soundboard_sound for soundboard_sound in soundboard_sounds})
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


def test__Guild__update_attributes():
    """
    Tests whether ``Guild._update_attributes`` works as intended.
    """
    guild_id = 2023062200100
    
    old_afk_channel_id = 202306220101
    old_afk_timeout = 1800
    old_approximate_online_count = 69
    old_approximate_user_count = 70
    old_available = True
    old_banner = Icon(IconType.animated, 12)
    old_boost_count = 3
    old_boost_progress_bar_enabled = True
    old_content_filter = ContentFilterLevel.no_role
    old_description = 'Koishi'
    old_discovery_splash = Icon(IconType.animated, 14)
    old_features = [GuildFeature.animated_icon]
    old_hub_type = HubType.college
    old_icon = Icon(IconType.animated, 16)
    old_invite_splash = Icon(IconType.animated, 18)
    old_max_presences = 420
    old_max_stage_channel_video_users = 421
    old_max_users = 422
    old_max_voice_channel_video_users = 423
    old_message_notification = MessageNotificationLevel.no_messages
    old_mfa = MFA.elevated
    old_name = 'Komeiji'
    old_nsfw_level = NsfwLevel.explicit
    old_owner_id = 202306220102
    old_preferred_locale = Locale.finnish
    old_premium_tier = 1
    old_public_updates_channel_id = 202306220103
    old_rules_channel_id = 202306220104
    old_safety_alerts_channel_id = 202306220105
    old_system_channel_id = 202306220106
    old_system_channel_flags = SystemChannelFlag(12)
    old_vanity_code = 'koi'
    old_verification_level = VerificationLevel.medium
    old_widget_channel_id = 202306220107
    old_widget_enabled = True
    
    new_afk_channel_id = 202306220108
    new_afk_timeout = 60
    new_approximate_online_count = 169
    new_approximate_user_count = 170
    new_available = False
    new_banner = Icon(IconType.animated, 112)
    new_boost_count = 13
    new_boost_progress_bar_enabled = False
    new_content_filter = ContentFilterLevel.everyone
    new_description = 'Orin'
    new_discovery_splash = Icon(IconType.animated, 114)
    new_features = [GuildFeature.animated_banner]
    new_hub_type = HubType.high_school
    new_icon = Icon(IconType.animated, 116)
    new_invite_splash = Icon(IconType.animated, 118)
    new_max_presences = 1420
    new_max_stage_channel_video_users = 1421
    new_max_users = 1422
    new_max_voice_channel_video_users = 1423
    new_message_notification = MessageNotificationLevel.only_mentions
    new_mfa = MFA.none
    new_name = 'Okuu'
    new_nsfw_level = NsfwLevel.safe
    new_owner_id = 202306220109
    new_preferred_locale = Locale.dutch
    new_premium_tier = 2
    new_public_updates_channel_id = 202306220110
    new_rules_channel_id = 202306220111
    new_safety_alerts_channel_id = 202306220112
    new_system_channel_id = 202306220113
    new_system_channel_flags = SystemChannelFlag(11)
    new_vanity_code = 'dancing'
    new_verification_level = VerificationLevel.high
    new_widget_channel_id = 202306220114
    new_widget_enabled = False
    
    
    guild = Guild.precreate(
        guild_id,
        afk_channel_id = old_afk_channel_id,
        afk_timeout = old_afk_timeout,
        approximate_online_count = old_approximate_online_count,
        approximate_user_count = old_approximate_user_count,
        available = old_available,
        banner = old_banner,
        boost_count = old_boost_count,
        boost_progress_bar_enabled = old_boost_progress_bar_enabled,
        content_filter = old_content_filter,
        description = old_description,
        discovery_splash = old_discovery_splash,
        features = old_features,
        hub_type = old_hub_type,
        icon = old_icon,
        invite_splash = old_invite_splash,
        max_presences = old_max_presences,
        max_stage_channel_video_users = old_max_stage_channel_video_users,
        max_users = old_max_users,
        max_voice_channel_video_users = old_max_voice_channel_video_users,
        message_notification = old_message_notification,
        mfa = old_mfa,
        name = old_name,
        nsfw_level = old_nsfw_level,
        owner_id = old_owner_id,
        preferred_locale = old_preferred_locale,
        premium_tier = old_premium_tier,
        public_updates_channel_id = old_public_updates_channel_id,
        rules_channel_id = old_rules_channel_id,
        safety_alerts_channel_id = old_safety_alerts_channel_id,
        system_channel_id = old_system_channel_id,
        system_channel_flags = old_system_channel_flags,
        vanity_code = old_vanity_code,
        verification_level = old_verification_level,
        widget_channel_id = old_widget_channel_id,
        widget_enabled = old_widget_enabled,
    )
    
    data = {
        'afk_channel_id': str(new_afk_channel_id),
        'afk_timeout': new_afk_timeout,
        'approximate_presence_count': new_approximate_online_count,
        'approximate_member_count': new_approximate_user_count,
        'unavailable': not new_available,
        'premium_progress_bar_enabled': new_boost_progress_bar_enabled,
        'premium_subscription_count': new_boost_count,
        'explicit_content_filter': new_content_filter.value,
        'description': new_description,
        'features': [feature.value for feature in new_features],
        'hub_type': new_hub_type.value,
        'max_presences': new_max_presences,
        'max_stage_video_channel_users': new_max_stage_channel_video_users,
        'max_members': new_max_users,
        'max_video_channel_users': new_max_voice_channel_video_users,
        'default_message_notifications': new_message_notification.value,
        'mfa_level': new_mfa.value,
        'name': new_name,
        'nsfw_level': new_nsfw_level.value,
        'owner_id': str(new_owner_id),
        'preferred_locale': new_preferred_locale.value,
        'premium_tier': new_premium_tier,
        'public_updates_channel_id': str(new_public_updates_channel_id),
        'rules_channel_id': str(new_rules_channel_id),
        'safety_alerts_channel_id': str(new_safety_alerts_channel_id),
        'system_channel_flags': int(new_system_channel_flags),
        'system_channel_id': str(new_system_channel_id),
        'vanity_url_code': new_vanity_code,
        'verification_level': new_verification_level.value,
        'widget_channel_id': str(new_widget_channel_id),
        'widget_enabled': new_widget_enabled,
        'icon': new_icon.as_base_16_hash,
        'banner': new_banner.as_base_16_hash,
        'discovery_splash': new_discovery_splash.as_base_16_hash,
        'splash': new_invite_splash.as_base_16_hash,
    }
    
    guild._update_attributes(data)
    
    vampytest.assert_eq(guild.afk_channel_id, new_afk_channel_id)
    vampytest.assert_eq(guild.afk_timeout, new_afk_timeout)
    vampytest.assert_eq(guild.approximate_online_count, new_approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, new_approximate_user_count)
    vampytest.assert_eq(guild.available, new_available)
    vampytest.assert_eq(guild.banner, new_banner)
    vampytest.assert_eq(guild.boost_count, new_boost_count)
    vampytest.assert_eq(guild.boost_progress_bar_enabled, new_boost_progress_bar_enabled)
    vampytest.assert_is(guild.content_filter, new_content_filter)
    vampytest.assert_eq(guild.description, new_description)
    vampytest.assert_eq(guild.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(guild.features, tuple(new_features))
    vampytest.assert_is(guild.hub_type, new_hub_type)
    vampytest.assert_eq(guild.icon, new_icon)
    vampytest.assert_eq(guild.invite_splash, new_invite_splash)
    vampytest.assert_eq(guild.max_presences, new_max_presences)
    vampytest.assert_eq(guild.max_stage_channel_video_users, new_max_stage_channel_video_users)
    vampytest.assert_eq(guild.max_users, new_max_users)
    vampytest.assert_eq(guild.max_voice_channel_video_users, new_max_voice_channel_video_users)
    vampytest.assert_is(guild.message_notification, new_message_notification)
    vampytest.assert_is(guild.mfa, new_mfa)
    vampytest.assert_eq(guild.name, new_name)
    vampytest.assert_is(guild.nsfw_level, new_nsfw_level)
    vampytest.assert_eq(guild.owner_id, new_owner_id)
    vampytest.assert_is(guild.preferred_locale, new_preferred_locale)
    vampytest.assert_eq(guild.premium_tier, new_premium_tier)
    vampytest.assert_eq(guild.public_updates_channel_id, new_public_updates_channel_id)
    vampytest.assert_eq(guild.rules_channel_id, new_rules_channel_id)
    vampytest.assert_eq(guild.safety_alerts_channel_id, new_safety_alerts_channel_id)
    vampytest.assert_eq(guild.system_channel_id, new_system_channel_id)
    vampytest.assert_eq(guild.system_channel_flags, new_system_channel_flags)
    vampytest.assert_eq(guild.vanity_code, new_vanity_code)
    vampytest.assert_eq(guild.verification_level, new_verification_level)
    vampytest.assert_eq(guild.widget_channel_id, new_widget_channel_id)
    vampytest.assert_eq(guild.widget_enabled, new_widget_enabled)


def test__Guild__update_counts_only():
    """
    Tests whether ``Guild._update_counts_only`` works as intended.
    """
    guild_id = 2023062200115
    
    old_approximate_online_count = 69
    old_approximate_user_count = 70
    
    new_approximate_online_count = 169
    new_approximate_user_count = 170
    
    
    guild = Guild.precreate(
        guild_id,
        approximate_online_count = old_approximate_online_count,
        approximate_user_count = old_approximate_user_count,
    )
    
    data = {
        'approximate_presence_count': new_approximate_online_count,
        'approximate_member_count': new_approximate_user_count,
    }
    
    guild._update_attributes(data)
    
    vampytest.assert_eq(guild.approximate_online_count, new_approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, new_approximate_user_count)



def test__Guild__difference_update_attributes():
    """
    Tests whether ``Guild._difference_update_attributes`` works as intended.
    """
    guild_id = 2023062200116
    
    old_afk_channel_id = 202306220117
    old_afk_timeout = 1800
    old_approximate_online_count = 69
    old_approximate_user_count = 70
    old_available = True
    old_banner = Icon(IconType.animated, 12)
    old_boost_count = 3
    old_boost_progress_bar_enabled = True
    old_content_filter = ContentFilterLevel.no_role
    old_description = 'Koishi'
    old_discovery_splash = Icon(IconType.animated, 14)
    old_features = [GuildFeature.animated_icon]
    old_hub_type = HubType.college
    old_icon = Icon(IconType.animated, 16)
    old_invite_splash = Icon(IconType.animated, 18)
    old_max_presences = 420
    old_max_stage_channel_video_users = 421
    old_max_users = 422
    old_max_voice_channel_video_users = 423
    old_message_notification = MessageNotificationLevel.no_messages
    old_mfa = MFA.elevated
    old_name = 'Komeiji'
    old_nsfw_level = NsfwLevel.explicit
    old_owner_id = 202306220118
    old_preferred_locale = Locale.finnish
    old_premium_tier = 1
    old_public_updates_channel_id = 202306220119
    old_rules_channel_id = 202306220120
    old_safety_alerts_channel_id = 202306220121
    old_system_channel_id = 202306220122
    old_system_channel_flags = SystemChannelFlag(12)
    old_vanity_code = 'koi'
    old_verification_level = VerificationLevel.medium
    old_widget_channel_id = 202306220123
    old_widget_enabled = True
    
    new_afk_channel_id = 202306220124
    new_afk_timeout = 60
    new_approximate_online_count = 169
    new_approximate_user_count = 170
    new_available = False
    new_banner = Icon(IconType.animated, 112)
    new_boost_count = 13
    new_boost_progress_bar_enabled = False
    new_content_filter = ContentFilterLevel.everyone
    new_description = 'Orin'
    new_discovery_splash = Icon(IconType.animated, 114)
    new_features = [GuildFeature.animated_banner]
    new_hub_type = HubType.high_school
    new_icon = Icon(IconType.animated, 116)
    new_invite_splash = Icon(IconType.animated, 118)
    new_max_presences = 1420
    new_max_stage_channel_video_users = 1421
    new_max_users = 1422
    new_max_voice_channel_video_users = 1423
    new_message_notification = MessageNotificationLevel.only_mentions
    new_mfa = MFA.none
    new_name = 'Okuu'
    new_nsfw_level = NsfwLevel.safe
    new_owner_id = 202306220125
    new_preferred_locale = Locale.dutch
    new_premium_tier = 2
    new_public_updates_channel_id = 202306220126
    new_rules_channel_id = 202306220127
    new_safety_alerts_channel_id = 202306220128
    new_system_channel_id = 202306220129
    new_system_channel_flags = SystemChannelFlag(11)
    new_vanity_code = 'dancing'
    new_verification_level = VerificationLevel.high
    new_widget_channel_id = 202306220130
    new_widget_enabled = False
    
    
    guild = Guild.precreate(
        guild_id,
        afk_channel_id = old_afk_channel_id,
        afk_timeout = old_afk_timeout,
        approximate_online_count = old_approximate_online_count,
        approximate_user_count = old_approximate_user_count,
        available = old_available,
        banner = old_banner,
        boost_count = old_boost_count,
        boost_progress_bar_enabled = old_boost_progress_bar_enabled,
        content_filter = old_content_filter,
        description = old_description,
        discovery_splash = old_discovery_splash,
        features = old_features,
        hub_type = old_hub_type,
        icon = old_icon,
        invite_splash = old_invite_splash,
        max_presences = old_max_presences,
        max_stage_channel_video_users = old_max_stage_channel_video_users,
        max_users = old_max_users,
        max_voice_channel_video_users = old_max_voice_channel_video_users,
        message_notification = old_message_notification,
        mfa = old_mfa,
        name = old_name,
        nsfw_level = old_nsfw_level,
        owner_id = old_owner_id,
        preferred_locale = old_preferred_locale,
        premium_tier = old_premium_tier,
        public_updates_channel_id = old_public_updates_channel_id,
        rules_channel_id = old_rules_channel_id,
        safety_alerts_channel_id = old_safety_alerts_channel_id,
        system_channel_id = old_system_channel_id,
        system_channel_flags = old_system_channel_flags,
        vanity_code = old_vanity_code,
        verification_level = old_verification_level,
        widget_channel_id = old_widget_channel_id,
        widget_enabled = old_widget_enabled,
    )
    
    data = {
        'afk_channel_id': str(new_afk_channel_id),
        'afk_timeout': new_afk_timeout,
        'approximate_presence_count': new_approximate_online_count,
        'approximate_member_count': new_approximate_user_count,
        'unavailable': not new_available,
        'premium_progress_bar_enabled': new_boost_progress_bar_enabled,
        'premium_subscription_count': new_boost_count,
        'explicit_content_filter': new_content_filter.value,
        'description': new_description,
        'features': [feature.value for feature in new_features],
        'hub_type': new_hub_type.value,
        'max_presences': new_max_presences,
        'max_stage_video_channel_users': new_max_stage_channel_video_users,
        'max_members': new_max_users,
        'max_video_channel_users': new_max_voice_channel_video_users,
        'default_message_notifications': new_message_notification.value,
        'mfa_level': new_mfa.value,
        'name': new_name,
        'nsfw_level': new_nsfw_level.value,
        'owner_id': str(new_owner_id),
        'preferred_locale': new_preferred_locale.value,
        'premium_tier': new_premium_tier,
        'public_updates_channel_id': str(new_public_updates_channel_id),
        'rules_channel_id': str(new_rules_channel_id),
        'safety_alerts_channel_id': str(new_safety_alerts_channel_id),
        'system_channel_flags': int(new_system_channel_flags),
        'system_channel_id': str(new_system_channel_id),
        'vanity_url_code': new_vanity_code,
        'verification_level': new_verification_level.value,
        'widget_channel_id': str(new_widget_channel_id),
        'widget_enabled': new_widget_enabled,
        'icon': new_icon.as_base_16_hash,
        'banner': new_banner.as_base_16_hash,
        'discovery_splash': new_discovery_splash.as_base_16_hash,
        'splash': new_invite_splash.as_base_16_hash,
    }
    
    old_attributes = guild._difference_update_attributes(data)
    
    vampytest.assert_eq(guild.afk_channel_id, new_afk_channel_id)
    vampytest.assert_eq(guild.afk_timeout, new_afk_timeout)
    vampytest.assert_eq(guild.approximate_online_count, new_approximate_online_count)
    vampytest.assert_eq(guild.approximate_user_count, new_approximate_user_count)
    vampytest.assert_eq(guild.available, new_available)
    vampytest.assert_eq(guild.banner, new_banner)
    vampytest.assert_eq(guild.boost_count, new_boost_count)
    vampytest.assert_eq(guild.boost_progress_bar_enabled, new_boost_progress_bar_enabled)
    vampytest.assert_is(guild.content_filter, new_content_filter)
    vampytest.assert_eq(guild.description, new_description)
    vampytest.assert_eq(guild.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(guild.features, tuple(new_features))
    vampytest.assert_is(guild.hub_type, new_hub_type)
    vampytest.assert_eq(guild.icon, new_icon)
    vampytest.assert_eq(guild.invite_splash, new_invite_splash)
    vampytest.assert_eq(guild.max_presences, new_max_presences)
    vampytest.assert_eq(guild.max_stage_channel_video_users, new_max_stage_channel_video_users)
    vampytest.assert_eq(guild.max_users, new_max_users)
    vampytest.assert_eq(guild.max_voice_channel_video_users, new_max_voice_channel_video_users)
    vampytest.assert_is(guild.message_notification, new_message_notification)
    vampytest.assert_is(guild.mfa, new_mfa)
    vampytest.assert_eq(guild.name, new_name)
    vampytest.assert_is(guild.nsfw_level, new_nsfw_level)
    vampytest.assert_eq(guild.owner_id, new_owner_id)
    vampytest.assert_is(guild.preferred_locale, new_preferred_locale)
    vampytest.assert_eq(guild.premium_tier, new_premium_tier)
    vampytest.assert_eq(guild.public_updates_channel_id, new_public_updates_channel_id)
    vampytest.assert_eq(guild.rules_channel_id, new_rules_channel_id)
    vampytest.assert_eq(guild.safety_alerts_channel_id, new_safety_alerts_channel_id)
    vampytest.assert_eq(guild.system_channel_id, new_system_channel_id)
    vampytest.assert_eq(guild.system_channel_flags, new_system_channel_flags)
    vampytest.assert_eq(guild.vanity_code, new_vanity_code)
    vampytest.assert_eq(guild.verification_level, new_verification_level)
    vampytest.assert_eq(guild.widget_channel_id, new_widget_channel_id)
    vampytest.assert_eq(guild.widget_enabled, new_widget_enabled)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'afk_channel_id': old_afk_channel_id,
            'afk_timeout': old_afk_timeout,
            # 'approximate_online_count': old_approximate_online_count,
            # 'approximate_user_count': old_approximate_user_count,
            'available': old_available,
            'banner': old_banner,
            'boost_count': old_boost_count,
            'boost_progress_bar_enabled': old_boost_progress_bar_enabled,
            'content_filter': old_content_filter,
            'description': old_description,
            'discovery_splash': old_discovery_splash,
            'features': tuple(old_features),
            'hub_type': old_hub_type,
            'icon': old_icon,
            'invite_splash': old_invite_splash,
            'max_presences': old_max_presences,
            'max_stage_channel_video_users': old_max_stage_channel_video_users,
            'max_users': old_max_users,
            'max_voice_channel_video_users': old_max_voice_channel_video_users,
            'message_notification': old_message_notification,
            'mfa': old_mfa,
            'name': old_name,
            'nsfw_level': old_nsfw_level,
            'owner_id': old_owner_id,
            'preferred_locale': old_preferred_locale,
            'premium_tier': old_premium_tier,
            'public_updates_channel_id': old_public_updates_channel_id,
            'rules_channel_id': old_rules_channel_id,
            'safety_alerts_channel_id': old_safety_alerts_channel_id,
            'system_channel_id': old_system_channel_id,
            'system_channel_flags': old_system_channel_flags,
            'vanity_code': old_vanity_code,
            'verification_level': old_verification_level,
            'widget_channel_id': old_widget_channel_id,
            'widget_enabled': old_widget_enabled,
        }
    )
