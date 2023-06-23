import vampytest
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
from ....sticker import Sticker, StickerFormat
from ....user import GuildProfile, User, VoiceState

from ...embedded_activity_state import EmbeddedActivityState

from ..emoji_counts import EmojiCounts
from ..flags import SystemChannelFlag
from ..guild import Guild
from ..guild_premium_perks import GuildPremiumPerks, TIER_0, TIER_MAX
from ..preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
)
from ..sticker_counts import StickerCounts

from .test__Guild__constructor import _assert_fields_set


def test__Guild__copy():
    """
    Tests whether ``Guild.copy`` works as intended.
    """
    afk_channel_id = 202306230000
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
    owner_id = 202306230001
    preferred_locale = Locale.finnish
    public_updates_channel_id = 202306230002
    rules_channel_id = 202306230004
    safety_alerts_channel_id = 202306230003
    system_channel_id = 202306230005
    system_channel_flags = SystemChannelFlag(12)
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    widget_channel_id = 202306230006
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
    
    copy = guild.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild, copy)
    vampytest.assert_eq(guild, copy)


def test__Guild__copy_with__0():
    """
    Tests whether ``Guild.copy_with`` works as intended.
    
    Case: No fields given.
    """
    afk_channel_id = 202306230007
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
    owner_id = 202306230008
    preferred_locale = Locale.finnish
    public_updates_channel_id = 202306230009
    rules_channel_id = 202306230010
    safety_alerts_channel_id = 202306230011
    system_channel_id = 202306230012
    system_channel_flags = SystemChannelFlag(12)
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    widget_channel_id = 202306230013
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
    
    copy = guild.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild, copy)
    vampytest.assert_eq(guild, copy)


def test__Guild__copy_with__1():
    """
    Tests whether ``Guild.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_afk_channel_id = 202306230014
    old_afk_timeout = 1800
    old_banner = Icon(IconType.animated, 12)
    old_boost_progress_bar_enabled = True
    old_content_filter = ContentFilterLevel.no_role
    old_description = 'Koishi'
    old_discovery_splash = Icon(IconType.animated, 14)
    old_features = [GuildFeature.animated_icon]
    old_hub_type = HubType.college
    old_icon = Icon(IconType.animated, 16)
    old_invite_splash = Icon(IconType.animated, 18)
    old_message_notification = MessageNotificationLevel.no_messages
    old_mfa = MFA.elevated
    old_name = 'Komeiji'
    old_nsfw_level = NsfwLevel.explicit
    old_owner_id = 202306230015
    old_preferred_locale = Locale.finnish
    old_public_updates_channel_id = 202306230016
    old_rules_channel_id = 202306230017
    old_safety_alerts_channel_id = 202306230018
    old_system_channel_id = 202306230019
    old_system_channel_flags = SystemChannelFlag(12)
    old_vanity_code = 'koi'
    old_verification_level = VerificationLevel.medium
    old_widget_channel_id = 202306230020
    old_widget_enabled = True
    
    new_afk_channel_id = 202306230021
    new_afk_timeout = 60
    new_banner = Icon(IconType.animated, 112)
    new_boost_progress_bar_enabled = False
    new_content_filter = ContentFilterLevel.everyone
    new_description = 'Okuu'
    new_discovery_splash = Icon(IconType.animated, 114)
    new_features = [GuildFeature.animated_banner]
    new_hub_type = HubType.high_school
    new_icon = Icon(IconType.animated, 116)
    new_invite_splash = Icon(IconType.animated, 118)
    new_message_notification = MessageNotificationLevel.all_messages
    new_mfa = MFA.none
    new_name = 'Orin'
    new_nsfw_level = NsfwLevel.safe
    new_owner_id = 202306230021
    new_preferred_locale = Locale.dutch
    new_public_updates_channel_id = 202306230022
    new_rules_channel_id = 202306230023
    new_safety_alerts_channel_id = 202306230024
    new_system_channel_id = 202306230025
    new_system_channel_flags = SystemChannelFlag(11)
    new_vanity_code = 'satori'
    new_verification_level = VerificationLevel.high
    new_widget_channel_id = 202306230026
    new_widget_enabled = False
    
    guild = Guild(
        afk_channel_id = old_afk_channel_id,
        afk_timeout = old_afk_timeout,
        banner = old_banner,
        boost_progress_bar_enabled = old_boost_progress_bar_enabled,
        content_filter = old_content_filter,
        description = old_description,
        discovery_splash = old_discovery_splash,
        features = old_features,
        hub_type = old_hub_type,
        icon = old_icon,
        invite_splash = old_invite_splash,
        message_notification = old_message_notification,
        mfa = old_mfa,
        name = old_name,
        nsfw_level = old_nsfw_level,
        owner_id = old_owner_id,
        preferred_locale = old_preferred_locale,
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
    
    copy = guild.copy_with(
        afk_channel_id = new_afk_channel_id,
        afk_timeout = new_afk_timeout,
        banner = new_banner,
        boost_progress_bar_enabled = new_boost_progress_bar_enabled,
        content_filter = new_content_filter,
        description = new_description,
        discovery_splash = new_discovery_splash,
        features = new_features,
        hub_type = new_hub_type,
        icon = new_icon,
        invite_splash = new_invite_splash,
        message_notification = new_message_notification,
        mfa = new_mfa,
        name = new_name,
        nsfw_level = new_nsfw_level,
        owner_id = new_owner_id,
        preferred_locale = new_preferred_locale,
        public_updates_channel_id = new_public_updates_channel_id,
        rules_channel_id = new_rules_channel_id,
        safety_alerts_channel_id = new_safety_alerts_channel_id,
        system_channel_id = new_system_channel_id,
        system_channel_flags = new_system_channel_flags,
        vanity_code = new_vanity_code,
        verification_level = new_verification_level,
        widget_channel_id = new_widget_channel_id,
        widget_enabled = new_widget_enabled,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild, copy)
    vampytest.assert_ne(guild, copy)


    vampytest.assert_eq(copy.afk_channel_id, new_afk_channel_id)
    vampytest.assert_eq(copy.afk_timeout, new_afk_timeout)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.boost_progress_bar_enabled, new_boost_progress_bar_enabled)
    vampytest.assert_is(copy.content_filter, new_content_filter)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(copy.features, tuple(new_features))
    vampytest.assert_is(copy.hub_type, new_hub_type)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.invite_splash, new_invite_splash)
    vampytest.assert_is(copy.message_notification, new_message_notification)
    vampytest.assert_is(copy.mfa, new_mfa)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.nsfw_level, new_nsfw_level)
    vampytest.assert_eq(copy.owner_id, new_owner_id)
    vampytest.assert_is(copy.preferred_locale, new_preferred_locale)
    vampytest.assert_eq(copy.public_updates_channel_id, new_public_updates_channel_id)
    vampytest.assert_eq(copy.rules_channel_id, new_rules_channel_id)
    vampytest.assert_eq(copy.safety_alerts_channel_id, new_safety_alerts_channel_id)
    vampytest.assert_eq(copy.system_channel_id, new_system_channel_id)
    vampytest.assert_eq(copy.system_channel_flags, new_system_channel_flags)
    vampytest.assert_eq(copy.vanity_code, new_vanity_code)
    vampytest.assert_eq(copy.verification_level, new_verification_level)
    vampytest.assert_eq(copy.widget_channel_id, new_widget_channel_id)
    vampytest.assert_eq(copy.widget_enabled, new_widget_enabled)


def test__Guild__nsfw__0():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: `NsfwLevel.safe`.
    """
    nsfw_level = NsfwLevel.safe
    guild = Guild.precreate(202208270000, nsfw_level = nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)


def test__Guild__nsfw__1():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: `NsfwLevel.explicit`.
    """
    nsfw_level = NsfwLevel.explicit
    guild = Guild.precreate(202208270001, nsfw_level = nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)


def test__Guild__iter_features():
    """
    Tests whether ``Guild.iter_features`` works as intended.
    """
    feature_0 = GuildFeature.animated_icon
    feature_1 = GuildFeature.animated_banner
    
    for guild, expected_output in (
        (Guild.precreate(202305290002, features = None), set()),
        (Guild.precreate(202305290003, features = [feature_0]), {feature_0}),
        (Guild.precreate(202305290004, features = [feature_0, feature_1]), {feature_0, feature_1}),
    ):
        vampytest.assert_eq({*guild.iter_features()}, expected_output)


def test__Guild__has_feature():
    """
    Tests whether ``Guild.has_feature`` works as intended.
    """
    feature = GuildFeature.animated_icon
    for guild, expected_output in (
        (Guild.precreate(202212190038, features = []), False),
        (Guild.precreate(202212200020, features = [GuildFeature.animated_banner]), False),
        (Guild.precreate(202212200021, features = [feature]), True),
        (Guild.precreate(202212200022, features = [GuildFeature.animated_banner, feature]), True),
    ):
        vampytest.assert_eq(guild.has_feature(feature), expected_output)


def test__Guild__premium_perks():
    """
    Tests whether ``Guild.premium_perks`` works as intended.
    """
    premium_tier = 2
    
    guild = Guild.precreate(202212190039, premium_tier = premium_tier)
    premium_perks = guild.premium_perks
    vampytest.assert_instance(premium_perks, GuildPremiumPerks)
    vampytest.assert_eq(premium_perks.tier, premium_tier)


def test__Guild__emoji_limit():
    """
    Tests whether ``Guild.emoji_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200000, premium_tier = 0), TIER_0.emoji_limit),
        (Guild.precreate(202212200001, premium_tier = TIER_MAX.tier), TIER_MAX.emoji_limit),
        (Guild.precreate(202212200002, premium_tier = 1, features = [GuildFeature.more_emoji]), 200),
        (
            Guild.precreate(202212200003, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_emoji]),
            TIER_MAX.emoji_limit,
        ),
    ):
        vampytest.assert_eq(guild.emoji_limit, expected_value)


def test__Guild__bitrate_limit():
    """
    Tests whether ``Guild.bitrate_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200004, premium_tier = 0), TIER_0.bitrate_limit),
        (Guild.precreate(202212200005, premium_tier = TIER_MAX.tier), TIER_MAX.bitrate_limit),
        (Guild.precreate(202212200006, premium_tier = 1, features = [GuildFeature.vip_voice_regions]), 128000),
        (
            Guild.precreate(202212200007, premium_tier = TIER_MAX.tier, features = [GuildFeature.vip_voice_regions]),
            TIER_MAX.bitrate_limit,
        ),
    ):
        vampytest.assert_eq(guild.bitrate_limit, expected_value)


def test__Guild__upload_limit():
    """
    Tests whether ``Guild.upload_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200008, premium_tier = 0), TIER_0.upload_limit),
        (Guild.precreate(202212200009, premium_tier = TIER_MAX.tier), TIER_MAX.upload_limit),
    ):
        vampytest.assert_eq(guild.upload_limit, expected_value)


def test__Guild__sticker_limit():
    """
    Tests whether ``Guild.sticker_limit`` works as intended.
    """
    for guild, expected_value in (
        (Guild.precreate(202212200010, premium_tier = 0), TIER_0.sticker_limit),
        (Guild.precreate(202212200011, premium_tier = TIER_MAX.tier), TIER_MAX.sticker_limit),
        (Guild.precreate(202212200012, premium_tier = 1, features = [GuildFeature.more_sticker]), 30),
        (
            Guild.precreate(202212200013, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_sticker]),
            TIER_MAX.sticker_limit,
        ),
    ):
        vampytest.assert_eq(guild.sticker_limit, expected_value)


def test__Guild__emoji_counts():
    """
    Tests whether ``Guild.emoji_counts`` works as intended.
    """
    emoji_0 = Emoji.precreate(202212200014)
    emoji_1 = Emoji.precreate(202212200015, animated = True, managed = True)
    
    guild = Guild.precreate(202212200016)
    guild.emojis[emoji_0.id] = emoji_0
    guild.emojis[emoji_1.id] = emoji_1
    
    emoji_counts = guild.emoji_counts
    vampytest.assert_instance(emoji_counts, EmojiCounts)
    vampytest.assert_eq(emoji_counts.normal_static, 1)
    vampytest.assert_eq(emoji_counts.managed_animated, 1)
    

def test__Guild__sticker_counts():
    """
    Tests whether ``Guild.sticker_counts`` works as intended.
    """
    sticker_0 = Sticker.precreate(202212200017, sticker_format = StickerFormat.png)
    sticker_1 = Sticker.precreate(202212200018, sticker_format = StickerFormat.apng)
    
    guild = Guild.precreate(202212200019)
    guild.stickers[sticker_0.id] = sticker_0
    guild.stickers[sticker_1.id] = sticker_1
    
    sticker_counts = guild.sticker_counts
    vampytest.assert_instance(sticker_counts, StickerCounts)
    vampytest.assert_eq(sticker_counts.static, 1)
    vampytest.assert_eq(sticker_counts.animated, 1)


def test__Guild__soundboard_sounds_cached():
    """
    Tests whether ``Guild.soundboard_sounds_cached`` works as intended.
    """
    message = Guild.precreate(202305280013)
    
    output = message.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    message.soundboard_sounds_cached = True
    output = message.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)

    message.soundboard_sounds_cached = False
    output = message.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Guild__iter_soundboard_sounds():
    """
    Tests whether ``Guild.iter_soundboard_sounds`` works as intended.
    """
    sound_0 = SoundboardSound.precreate(202305300000, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300001, name = 'rin')
    
    for guild, expected_output in (
        (Guild.precreate(202305300002, soundboard_sounds = None), set()),
        (Guild.precreate(202305300003, soundboard_sounds = [sound_0]), {sound_0}),
        (Guild.precreate(202305300004, soundboard_sounds = [sound_0, sound_1]), {sound_0, sound_1}),
    ):
        vampytest.assert_eq({*guild.iter_soundboard_sounds()}, expected_output)


def test__Guild__get_soundboard_sound():
    """
    Tests whether ``Guild.get_soundboard_sound`` works as intended.
    """
    sound_0 = SoundboardSound.precreate(202305300005, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300006, name = 'rin')
    
    for guild, name, expected_output in (
        (Guild.precreate(202305300007, soundboard_sounds = None), 'rin', None),
        (Guild.precreate(202305300008, soundboard_sounds = [sound_0]), 'rin', None),
        (Guild.precreate(202305300009, soundboard_sounds = [sound_1]), 'rin', sound_1),
        (Guild.precreate(202305300010, soundboard_sounds = [sound_0, sound_1]), 'rin', sound_1),
    ):
        vampytest.assert_is(guild.get_soundboard_sound(name), expected_output)


def test__Guild__get_soundboard_sound_like():
    """
    Tests whether ``Guild.get_soundboard_sound_like`` works as intended.
    """
    sound_0 = SoundboardSound.precreate(202305300011, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300012, name = 'rin')
    
    for guild, name, expected_output in (
        (Guild.precreate(202305300013, soundboard_sounds = None), 'rin', None),
        (Guild.precreate(202305300014, soundboard_sounds = [sound_0]), 'rin', sound_0),
        (Guild.precreate(202305300015, soundboard_sounds = [sound_1]), 'rin', sound_1),
        (Guild.precreate(202305300016, soundboard_sounds = [sound_1]), 'orin', None),
        (Guild.precreate(202305300017, soundboard_sounds = [sound_0, sound_1]), 'rin', sound_1),
        (Guild.precreate(202305300018, soundboard_sounds = [sound_0, sound_1]), 'orin', sound_0),
        (Guild.precreate(202305300019, soundboard_sounds = [sound_0, sound_1]), 'okuu', None),
    ):
        vampytest.assert_is(guild.get_soundboard_sound_like(name), expected_output)


def test__Guild__get_soundboard_sounds_like():
    """
    Tests whether ``Guild.get_soundboard_sounds_like`` works as intended.
    """
    sound_0 = SoundboardSound.precreate(202305300020, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300021, name = 'rin')
    
    for guild, name, expected_output in (
        (Guild.precreate(202305300022, soundboard_sounds = None), 'rin', []),
        (Guild.precreate(202305300023, soundboard_sounds = [sound_0]), 'rin', [sound_0]),
        (Guild.precreate(202305300024, soundboard_sounds = [sound_1]), 'rin', [sound_1]),
        (Guild.precreate(202305300025, soundboard_sounds = [sound_1]), 'orin', []),
        (Guild.precreate(202305300026, soundboard_sounds = [sound_0, sound_1]), 'rin', [sound_1, sound_0]),
        (Guild.precreate(202305300027, soundboard_sounds = [sound_0, sound_1]), 'orin', [sound_0]),
        (Guild.precreate(202305300028, soundboard_sounds = [sound_0, sound_1]), 'okuu', []),
    ):
        vampytest.assert_eq(guild.get_soundboard_sounds_like(name), expected_output)
