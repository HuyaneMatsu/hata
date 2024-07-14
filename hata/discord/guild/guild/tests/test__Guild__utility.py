from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....activity import Activity
from ....bases import Icon, IconType
from ....channel import Channel, ChannelType
from ....client import Client
from ....emoji import Emoji
from ....localization import Locale
from ....permission import Permission
from ....permission.permission import PERMISSION_ALL, PERMISSION_NONE
from ....role import Role
from ....scheduled_event import ScheduledEvent
from ....soundboard import SoundboardSound
from ....stage import Stage
from ....sticker import Sticker, StickerFormat
from ....user import ClientUserBase, GuildProfile, User, VoiceState
from ....utils import is_url
from ....webhook import Webhook

from ...embedded_activity_state import EmbeddedActivityState

from ..constants import GUILD_STATE_MASK_CACHE_ALL, GUILD_STATE_MASK_CACHE_BOOSTERS
from ..emoji_counts import EmojiCounts
from ..flags import SystemChannelFlag
from ..guild import Guild
from ..guild_premium_perks import GuildPremiumPerks, TIER_0, TIER_MAX
from ..preinstanced import (
    ExplicitContentFilterLevel, GuildFeature, HubType, MfaLevel, MessageNotificationLevel, NsfwLevel, VerificationLevel
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
    explicit_content_filter_level = ExplicitContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    default_message_notification_level = MessageNotificationLevel.no_messages
    mfa_level = MfaLevel.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306230001
    locale = Locale.finnish
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
        explicit_content_filter_level = explicit_content_filter_level,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        hub_type = hub_type,
        icon = icon,
        invite_splash = invite_splash,
        default_message_notification_level = default_message_notification_level,
        mfa_level = mfa_level,
        name = name,
        nsfw_level = nsfw_level,
        owner_id = owner_id,
        locale = locale,
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
    explicit_content_filter_level = ExplicitContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    default_message_notification_level = MessageNotificationLevel.no_messages
    mfa_level = MfaLevel.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306230008
    locale = Locale.finnish
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
        explicit_content_filter_level = explicit_content_filter_level,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        hub_type = hub_type,
        icon = icon,
        invite_splash = invite_splash,
        default_message_notification_level = default_message_notification_level,
        mfa_level = mfa_level,
        name = name,
        nsfw_level = nsfw_level,
        owner_id = owner_id,
        locale = locale,
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
    old_explicit_content_filter_level = ExplicitContentFilterLevel.no_role
    old_description = 'Koishi'
    old_discovery_splash = Icon(IconType.animated, 14)
    old_features = [GuildFeature.animated_icon]
    old_hub_type = HubType.college
    old_icon = Icon(IconType.animated, 16)
    old_invite_splash = Icon(IconType.animated, 18)
    old_default_message_notification_level = MessageNotificationLevel.no_messages
    old_mfa_level = MfaLevel.elevated
    old_name = 'Komeiji'
    old_nsfw_level = NsfwLevel.explicit
    old_owner_id = 202306230015
    old_locale = Locale.finnish
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
    new_explicit_content_filter_level = ExplicitContentFilterLevel.everyone
    new_description = 'Okuu'
    new_discovery_splash = Icon(IconType.animated, 114)
    new_features = [GuildFeature.animated_banner]
    new_hub_type = HubType.high_school
    new_icon = Icon(IconType.animated, 116)
    new_invite_splash = Icon(IconType.animated, 118)
    new_default_message_notification_level = MessageNotificationLevel.all_messages
    new_mfa_level = MfaLevel.none
    new_name = 'Orin'
    new_nsfw_level = NsfwLevel.safe
    new_owner_id = 202306230021
    new_locale = Locale.dutch
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
        explicit_content_filter_level = old_explicit_content_filter_level,
        description = old_description,
        discovery_splash = old_discovery_splash,
        features = old_features,
        hub_type = old_hub_type,
        icon = old_icon,
        invite_splash = old_invite_splash,
        default_message_notification_level = old_default_message_notification_level,
        mfa_level = old_mfa_level,
        name = old_name,
        nsfw_level = old_nsfw_level,
        owner_id = old_owner_id,
        locale = old_locale,
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
        explicit_content_filter_level = new_explicit_content_filter_level,
        description = new_description,
        discovery_splash = new_discovery_splash,
        features = new_features,
        hub_type = new_hub_type,
        icon = new_icon,
        invite_splash = new_invite_splash,
        default_message_notification_level = new_default_message_notification_level,
        mfa_level = new_mfa_level,
        name = new_name,
        nsfw_level = new_nsfw_level,
        owner_id = new_owner_id,
        locale = new_locale,
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
    vampytest.assert_is(copy.explicit_content_filter_level, new_explicit_content_filter_level)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(copy.features, tuple(new_features))
    vampytest.assert_is(copy.hub_type, new_hub_type)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.invite_splash, new_invite_splash)
    vampytest.assert_is(copy.default_message_notification_level, new_default_message_notification_level)
    vampytest.assert_is(copy.mfa_level, new_mfa_level)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.nsfw_level, new_nsfw_level)
    vampytest.assert_eq(copy.owner_id, new_owner_id)
    vampytest.assert_is(copy.locale, new_locale)
    vampytest.assert_eq(copy.public_updates_channel_id, new_public_updates_channel_id)
    vampytest.assert_eq(copy.rules_channel_id, new_rules_channel_id)
    vampytest.assert_eq(copy.safety_alerts_channel_id, new_safety_alerts_channel_id)
    vampytest.assert_eq(copy.system_channel_id, new_system_channel_id)
    vampytest.assert_eq(copy.system_channel_flags, new_system_channel_flags)
    vampytest.assert_eq(copy.vanity_code, new_vanity_code)
    vampytest.assert_eq(copy.verification_level, new_verification_level)
    vampytest.assert_eq(copy.widget_channel_id, new_widget_channel_id)
    vampytest.assert_eq(copy.widget_enabled, new_widget_enabled)


def test__Guild__delete__0():
    """
    Tests whether ``Guild._delete`` works as intended.
    
    Case: Client not in guild.
    """
    user_id = 202306230027
    client_id = 202306230028
    guild_id = 202306230029
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    client = Client(
        token = 'token_20230623_0000',
        client_id = client_id,
    )
    
    guild = Guild.precreate(guild_id, users = [user])
    
    try:
        guild._delete(client)
        
        vampytest.assert_in(guild_id, user.guild_profiles)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Guild__delete__1():
    """
    Tests whether ``Guild._delete`` works as intended.
    
    Case: Client is last client.
    """
    user_id = 202306230030
    client_id = 202306230031
    guild_id = 202306230032
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    client = Client(
        token = 'token_20230623_0001',
        client_id = client_id,
    )
    client.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(guild_id, users = [client, user])
    guild.clients.append(client)
    
    try:
        guild._delete(client)
        
        vampytest.assert_not_in(guild_id, user.guild_profiles)
        vampytest.assert_in(guild_id, client.guild_profiles)
        vampytest.assert_eq(guild.clients, [])
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Guild__delete__2():
    """
    Tests whether ``Guild._delete`` works as intended.
    
    Case: Client is not last
    """
    user_id = 202306230033
    client_id_0 = 202306230034
    client_id_1 = 202306230035
    guild_id = 202306230036
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    client_0 = Client(
        token = 'token_20230623_0001',
        client_id = client_id_0,
    )
    client_0.guild_profiles[guild_id] = GuildProfile()
    
    client_1 = Client(
        token = 'token_20230623_0002',
        client_id = client_id_1,
    )
    client_1.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(guild_id, users = [client_0, client_1, user])
    guild.clients.append(client_0)
    guild.clients.append(client_1)
    
    
    try:
        guild._delete(client_0)
        
        vampytest.assert_in(guild_id, user.guild_profiles)
        vampytest.assert_in(guild_id, client_0.guild_profiles)
        vampytest.assert_in(guild_id, client_1.guild_profiles)
        vampytest.assert_eq(guild.clients, [client_1])
        
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        
        client_1._delete()
        client_1 = None


@vampytest.call_with('shield')
@vampytest.call_with('banner1')
@vampytest.call_with('banner2')
@vampytest.call_with('banner3')
@vampytest.call_with('banner4')
def test__Guild__widget_url_as__passing(style):
    """
    Tests whether ``Guild.widget_url_as`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    style : `str`
        Widget style
    """
    guild = Guild.precreate(202306230037)
    widget_url = guild.widget_url_as(style)
    
    vampytest.assert_instance(widget_url, str)
    vampytest.assert_true(is_url(widget_url))


@vampytest.raising(ValueError)
@vampytest.call_with('shield1')
@vampytest.call_with('banner11')
@vampytest.call_with('banner5')
@vampytest.call_with('banner0')
def test__Guild__widget_url_as__value_error(style):
    """
    Tests whether ``Guild.widget_url_as`` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    style : `str`
        Widget style
    """
    guild = Guild.precreate(202306230038)
    widget_url = guild.widget_url_as(style)
    
    vampytest.assert_instance(widget_url, str)
    vampytest.assert_true(is_url(widget_url))


def test__Guild__widget_url():
    """
    Tests whether ``Guild.widget_url`` works as intended.
    """
    guild = Guild.precreate(202306230039)
    widget_url = guild.widget_url
    
    vampytest.assert_instance(widget_url, str)
    vampytest.assert_true(is_url(widget_url))
    

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


def _iter_options__iter_features():
    feature_0 = GuildFeature.animated_icon
    feature_1 = GuildFeature.animated_banner
    
    yield Guild.precreate(202305290002, features = None), set()
    yield Guild.precreate(202305290003, features = [feature_0]), {feature_0}
    yield Guild.precreate(202305290004, features = [feature_0, feature_1]), {feature_0, feature_1}


@vampytest._(vampytest.call_from(_iter_options__iter_features()).returning_last())
def test__Guild__iter_features(guild):
    """
    Tests whether ``Guild.iter_features`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iter the features of.
    
    Returns
    -------
    output : `set` of ``GuildFeature``
    """
    return {*guild.iter_features()}


def _iter_options__has_feature():
    feature = GuildFeature.animated_icon

    yield Guild.precreate(202212190038, features = []), feature, False
    yield Guild.precreate(202212200020, features = [GuildFeature.animated_banner]), feature, False
    yield Guild.precreate(202212200021, features = [feature]), feature, True
    yield Guild.precreate(202212200022, features = [GuildFeature.animated_banner, feature]), feature, True


@vampytest._(vampytest.call_from(_iter_options__has_feature()).returning_last())
def test__Guild__has_feature(guild, feature):
    """
    Tests whether ``Guild.has_feature`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to check the feature of.
    feature : ``GuildFeature``
        The feature to check for.
    
    Returns
    -------
    output : `bool`
    """
    return guild.has_feature(feature)


def test__Guild__premium_perks():
    """
    Tests whether ``Guild.premium_perks`` works as intended.
    """
    premium_tier = 2
    
    guild = Guild.precreate(202212190039, premium_tier = premium_tier)
    premium_perks = guild.premium_perks
    vampytest.assert_instance(premium_perks, GuildPremiumPerks)
    vampytest.assert_eq(premium_perks.tier, premium_tier)


def _iter_options__emoji_limit():
    yield Guild.precreate(202212200000, premium_tier = 0), TIER_0.emoji_limit
    yield Guild.precreate(202212200001, premium_tier = TIER_MAX.tier), TIER_MAX.emoji_limit
    yield Guild.precreate(202212200002, premium_tier = 1, features = [GuildFeature.more_emoji]), 200
    yield (
        Guild.precreate(202212200003, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_emoji]),
        TIER_MAX.emoji_limit,
    )
    

@vampytest._(vampytest.call_from(_iter_options__emoji_limit()).returning_last())
def test__Guild__emoji_limit(guild):
    """
    Tests whether ``Guild.emoji_limit`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its emoji limit of.
    
    Returns
    -------
    output : `int`
    """
    emoji_limit = guild.emoji_limit
    vampytest.assert_instance(emoji_limit, int)
    return emoji_limit


def _iter_options__bitrate_limit():
    yield Guild.precreate(202212200004, premium_tier = 0), TIER_0.bitrate_limit
    yield Guild.precreate(202212200005, premium_tier = TIER_MAX.tier), TIER_MAX.bitrate_limit
    yield Guild.precreate(202212200006, premium_tier = 1, features = [GuildFeature.vip_voice_regions]), 128000
    yield (
        Guild.precreate(202212200007, premium_tier = TIER_MAX.tier, features = [GuildFeature.vip_voice_regions]),
        TIER_MAX.bitrate_limit,
    )


@vampytest._(vampytest.call_from(_iter_options__bitrate_limit()).returning_last())
def test__Guild__bitrate_limit(guild):
    """
    Tests whether ``Guild.bitrate_limit`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its bitrate limit of.
    
    Returns
    -------
    output : `int`
    """
    bitrate_limit = guild.bitrate_limit
    vampytest.assert_instance(bitrate_limit, int)
    return bitrate_limit


def _iter_options__upload_limit():
    yield Guild.precreate(202212200008, premium_tier = 0), TIER_0.upload_limit
    yield Guild.precreate(202212200009, premium_tier = TIER_MAX.tier), TIER_MAX.upload_limit


@vampytest._(vampytest.call_from(_iter_options__upload_limit()).returning_last())
def test__Guild__upload_limit(guild):
    """
    Tests whether ``Guild.upload_limit`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its upload limit of.
    
    Returns
    -------
    output : `int`
    """
    upload_limit = guild.upload_limit
    vampytest.assert_instance(upload_limit, int)
    return upload_limit


def _iter_options__sticker_limit():
    yield Guild.precreate(202212200010, premium_tier = 0), TIER_0.sticker_limit
    yield Guild.precreate(202212200011, premium_tier = TIER_MAX.tier), TIER_MAX.sticker_limit
    yield Guild.precreate(202212200012, premium_tier = 1, features = [GuildFeature.more_sticker]), 30
    yield (
        Guild.precreate(202212200013, premium_tier = TIER_MAX.tier, features = [GuildFeature.more_sticker]),
        TIER_MAX.sticker_limit,
    )


@vampytest._(vampytest.call_from(_iter_options__sticker_limit()).returning_last())
def test__Guild__sticker_limit(guild):
    """
    Tests whether ``Guild.sticker_limit`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its sticker limit of.
    
    Returns
    -------
    output : `int`
    """
    sticker_limit = guild.sticker_limit
    vampytest.assert_instance(sticker_limit, int)
    return sticker_limit


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
    guild = Guild.precreate(202305280013)
    
    output = guild.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    guild.soundboard_sounds_cached = True
    output = guild.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)

    guild.soundboard_sounds_cached = False
    output = guild.soundboard_sounds_cached
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def _iter_options__iter_soundboard_sounds():
    sound_0 = SoundboardSound.precreate(202305300000, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300001, name = 'rin')
    
    
    yield Guild.precreate(202305300002, soundboard_sounds = None), set()
    yield Guild.precreate(202305300003, soundboard_sounds = [sound_0]), {sound_0}
    yield Guild.precreate(202305300004, soundboard_sounds = [sound_0, sound_1]), {sound_0, sound_1}


@vampytest._(vampytest.call_from(_iter_options__iter_soundboard_sounds()).returning_last())
def test__Guild__iter_soundboard_sounds(guild):
    """
    Tests whether ``Guild.iter_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iter its soundboard sounds of.
    
    Returns
    -------
    output : `set` of ``SoundboardSound``
    """
    return {*guild.iter_soundboard_sounds()}


def _iter_options__get_soundboard_sound():

    sound_0 = SoundboardSound.precreate(202305300005, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300006, name = 'rin')
    
    yield Guild.precreate(202305300007, soundboard_sounds = None), 'rin', None
    yield Guild.precreate(202305300008, soundboard_sounds = [sound_0]), 'rin', None
    yield Guild.precreate(202305300009, soundboard_sounds = [sound_1]), 'rin', sound_1
    yield Guild.precreate(202305300010, soundboard_sounds = [sound_0, sound_1]), 'rin', sound_1


@vampytest._(vampytest.call_from(_iter_options__get_soundboard_sound()).returning_last())
def test__Guild__get_soundboard_sound(guild, name):
    """
    Tests whether ``Guild.get_soundboard_sound`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the soundboard sound from.
    name : `str`
        Sound name to query.
    
    Returns
    -------
    output : `None`, ``SoundboardSound``
    """
    return guild.get_soundboard_sound(name)


def _iter_options__get_soundboard_sound_like():
    sound_0 = SoundboardSound.precreate(202305300011, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300012, name = 'rin')
    
    yield Guild.precreate(202305300013, soundboard_sounds = None), 'rin', None
    yield Guild.precreate(202305300014, soundboard_sounds = [sound_0]), 'rin', sound_0
    yield Guild.precreate(202305300015, soundboard_sounds = [sound_1]), 'rin', sound_1
    yield Guild.precreate(202305300016, soundboard_sounds = [sound_1]), 'orin', None
    yield Guild.precreate(202305300017, soundboard_sounds = [sound_0, sound_1]), 'rin', sound_1
    yield Guild.precreate(202305300018, soundboard_sounds = [sound_0, sound_1]), 'orin', sound_0
    yield Guild.precreate(202305300019, soundboard_sounds = [sound_0, sound_1]), 'okuu', None


@vampytest._(vampytest.call_from(_iter_options__get_soundboard_sound_like()).returning_last())
def test__Guild__get_soundboard_sound_like(guild, name):
    """
    Tests whether ``Guild.get_soundboard_sound_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the soundboard sound from.
    name : `str`
        Sound name to query.
    
    Returns
    -------
    output : `None`, ``SoundboardSound``
    """
    return guild.get_soundboard_sound_like(name)


def _iter_options__get_soundboard_sounds_like():
    sound_0 = SoundboardSound.precreate(202305300020, name = 'orin')
    sound_1 = SoundboardSound.precreate(202305300021, name = 'rin')
    
    
    yield Guild.precreate(202305300022, soundboard_sounds = None), 'rin', []
    yield Guild.precreate(202305300023, soundboard_sounds = [sound_0]), 'rin', [sound_0]
    yield Guild.precreate(202305300024, soundboard_sounds = [sound_1]), 'rin', [sound_1]
    yield Guild.precreate(202305300025, soundboard_sounds = [sound_1]), 'orin', []
    yield Guild.precreate(202305300026, soundboard_sounds = [sound_0, sound_1]), 'rin', [sound_1, sound_0]
    yield Guild.precreate(202305300027, soundboard_sounds = [sound_0, sound_1]), 'orin', [sound_0]
    yield Guild.precreate(202305300028, soundboard_sounds = [sound_0, sound_1]), 'okuu', []


@vampytest._(vampytest.call_from(_iter_options__get_soundboard_sounds_like()).returning_last())
def test__Guild__get_soundboard_sounds_like(guild, name):
    """
    Tests whether ``Guild.get_soundboard_sounds_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the soundboard sound from.
    name : `str`
        Sound name to query.
    
    Returns
    -------
    output : `list` of ``SoundboardSound``
    """
    return guild.get_soundboard_sounds_like(name)


def test__Guild__vanity_url__has_no():
    """
    Tests whether ``Guild.vanity_url`` works as intended.
    """
    guild = Guild.precreate(202306230130, vanity_code = None)
    vanity_url = guild.vanity_url
    
    vampytest.assert_is(vanity_url, None)


def test__Guild__vanity_url__has():
    """
    Tests whether ``Guild.vanity_url`` works as intended.
    """
    guild = Guild.precreate(202306230131, vanity_code = 'koishi')
    vanity_url = guild.vanity_url
    
    vampytest.assert_instance(vanity_url, str)
    vampytest.assert_true(is_url(vanity_url))


def test__Guild__widget_json_url():
    """
    Tests whether ``Guild.widget_json_url`` works as intended.
    """
    guild = Guild.precreate(202306230132)
    widget_json_url = guild.widget_json_url
    
    vampytest.assert_instance(widget_json_url, str)
    vampytest.assert_true(is_url(widget_json_url))


def test__Guild__default_role():
    """
    Tests whether ``Guild.default_role`` works as intended.
    """
    guild_id = 202306240000
    
    role = Role.precreate(guild_id)
    guild = Guild.precreate(guild_id, roles = [role])
    
    default_role = guild.default_role
    vampytest.assert_is(default_role, role)


def test__Guild__default_role__none():
    """
    Tests whether ``Guild.default_role`` works as intended.
    
    Case: Default role is missing
    """
    guild_id = 202306240001
    
    guild = Guild.precreate(guild_id)
    
    default_role = guild.default_role
    vampytest.assert_is(default_role, None)


def test__Guild__partial__true():
    """
    Tests whether ``Guild.partial`` works as intended.
    
    Case: `True`.
    """
    guild = Guild.precreate(202306240002)
    partial = guild.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_eq(partial, True)


def test__Guild__partial__false():
    """
    Tests whether ``Guild.partial`` works as intended.
    
    Case: `False`.
    """
    client = Client(
        token = 'token_20230624_0000',
    )
    
    guild = Guild.precreate(202306240003)
    guild.clients.append(client)
    
    try:
        partial = guild.partial
        vampytest.assert_instance(partial, bool)
        vampytest.assert_eq(partial, False)
    
    # Cleanup
    finally:
        client._delete()
        client = None
        

def test__Guild__invalidate_cache_permission():
    """
    Tests whether ``Guild._invalidate_cache_permission`` works as intended.
    """
    channel_id = 202306240004
    guild_id = 202306240005
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text)
    role = Role.precreate(guild_id, permissions = 8)
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role])
    
    client = Client(
        token = 'token_20230624_0001',
    )
    client.guild_profiles[guild_id] = GuildProfile()
    
    try:
        guild.cached_permissions_for(client)
        channel.cached_permissions_for(client)
        
        vampytest.assert_is_not(channel.metadata._cache_permission, None)
        vampytest.assert_is_not(guild._cache_permission, None)
        
        guild._invalidate_cache_permission()
        
        
        vampytest.assert_is(channel.metadata._cache_permission, None)
        vampytest.assert_is(guild._cache_permission, None)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Guild__owner():
    """
    Tests whether ``Guild.owner`` works as intended.
    """
    guild_id = 202306240006
    user_id = 202306240007
    
    guild = Guild.precreate(guild_id, owner_id = user_id)
    
    owner = guild.owner
    vampytest.assert_instance(owner, ClientUserBase)
    vampytest.assert_eq(owner.id, user_id)


def test__Guild__owner__none():
    """
    Tests whether ``Guild.owner`` works as intended.
    
    Case: No owner.
    """
    guild_id = 202306240008
    
    guild = Guild.precreate(guild_id)
    
    owner = guild.owner
    vampytest.assert_instance(owner, ClientUserBase)
    vampytest.assert_eq(owner.id, 0)


def _iter_options__get_emoji():
    emoji_0 = Emoji.precreate(202306240009, name = 'orin')
    emoji_1 = Emoji.precreate(202306240010, name = 'rin')
    
    yield Guild.precreate(202306240011, emojis = None), 'rin', None
    yield Guild.precreate(202306240012, emojis = [emoji_0]), 'rin', None
    yield Guild.precreate(202306240013, emojis = [emoji_1]), 'rin', emoji_1
    yield Guild.precreate(202306240014, emojis = [emoji_0, emoji_1]), 'rin', emoji_1


@vampytest._(vampytest.call_from(_iter_options__get_emoji()).returning_last())
def test__Guild__get_emoji(guild, name):
    """
    Tests whether ``Guild.get_emoji`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the emoji from.
    name : `str`
        Emoji name to query.
    
    Returns
    -------
    output : `None`, ``Emoji``
    """
    return guild.get_emoji(name)


def _iter_options__get_emoji_like():
    emoji_0 = Emoji.precreate(202306240015, name = 'orin')
    emoji_1 = Emoji.precreate(202306240016, name = 'rin')
    
    yield Guild.precreate(202306240017, emojis = None), 'rin', None
    yield Guild.precreate(202306240018, emojis = [emoji_0]), 'rin', emoji_0
    yield Guild.precreate(202306240019, emojis = [emoji_1]), 'rin', emoji_1
    yield Guild.precreate(202306240020, emojis = [emoji_1]), 'orin', None
    yield Guild.precreate(202306240021, emojis = [emoji_0, emoji_1]), 'rin', emoji_1
    yield Guild.precreate(202306240022, emojis = [emoji_0, emoji_1]), 'orin', emoji_0
    yield Guild.precreate(202306240023, emojis = [emoji_0, emoji_1]), 'okuu', None


@vampytest._(vampytest.call_from(_iter_options__get_emoji_like()).returning_last())
def test__Guild__get_emoji_like(guild, name):
    """
    Tests whether ``Guild.get_emoji_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the emoji from.
    name : `str`
        Emoji name to query.
    
    Returns
    -------
    output : `None`, ``Emoji``
    """
    return guild.get_emoji_like(name)


def _iter_options__get_emojis_like():
    emoji_0 = Emoji.precreate(202306240024, name = 'orin')
    emoji_1 = Emoji.precreate(202306240025, name = 'rin')
    
    yield Guild.precreate(202306240026, emojis = None), 'rin', []
    yield Guild.precreate(202306240027, emojis = [emoji_0]), 'rin', [emoji_0]
    yield Guild.precreate(202306240028, emojis = [emoji_1]), 'rin', [emoji_1]
    yield Guild.precreate(202306240029, emojis = [emoji_1]), 'orin', []
    yield Guild.precreate(202306240030, emojis = [emoji_0, emoji_1]), 'rin', [emoji_1, emoji_0]
    yield Guild.precreate(202306240031, emojis = [emoji_0, emoji_1]), 'orin', [emoji_0]
    yield Guild.precreate(202306240032, emojis = [emoji_0, emoji_1]), 'okuu', []


@vampytest._(vampytest.call_from(_iter_options__get_emojis_like()).returning_last())
def test__Guild__get_emojis_like(guild, name):
    """
    Tests whether ``Guild.get_emojis_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the emoji from.
    name : `str`
        Emoji name to query.
    
    Returns
    -------
    output : `list` of ``Emoji``
    """
    return guild.get_emojis_like(name)


def _iter_options__get_sticker():
    sticker_0 = Sticker.precreate(202306240033, name = 'orin')
    sticker_1 = Sticker.precreate(202306240034, name = 'rin')
    
    yield Guild.precreate(202306240035, stickers = None), 'rin', None
    yield Guild.precreate(202306240036, stickers = [sticker_0]), 'rin', None
    yield Guild.precreate(202306240037, stickers = [sticker_1]), 'rin', sticker_1
    yield Guild.precreate(202306240038, stickers = [sticker_0, sticker_1]), 'rin', sticker_1


@vampytest._(vampytest.call_from(_iter_options__get_sticker()).returning_last())
def test__Guild__get_sticker(guild, name):
    """
    Tests whether ``Guild.get_sticker`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the sticker from.
    name : `str`
        Sticker name to query.
    
    Returns
    -------
    output : `None`, ``Sticker``
    """
    return guild.get_sticker(name)


def _iter_options__get_sticker_like():
    sticker_0 = Sticker.precreate(202306240039, name = 'orin')
    sticker_1 = Sticker.precreate(202306240040, name = 'rin')
    sticker_2 = Sticker.precreate(202306260027, name = 'cat', tags = ['orin'])
    sticker_3 = Sticker.precreate(202306260028, name = 'cat', tags = ['rin'])
    sticker_4 = Sticker.precreate(202306260029, name = 'cat', tags = ['orin', 'rin'])
    
    yield Guild.precreate(202306240041, stickers = None), 'rin', None
    yield Guild.precreate(202306240042, stickers = [sticker_0]), 'rin', sticker_0
    yield Guild.precreate(202306240043, stickers = [sticker_1]), 'rin', sticker_1
    yield Guild.precreate(202306240044, stickers = [sticker_1]), 'orin', None
    yield Guild.precreate(202306240045, stickers = [sticker_0, sticker_1]), 'rin', sticker_1
    yield Guild.precreate(202306240046, stickers = [sticker_0, sticker_1]), 'orin', sticker_0
    yield Guild.precreate(202306240047, stickers = [sticker_0, sticker_1]), 'okuu', None
    yield Guild.precreate(202306260030, stickers = [sticker_2]), 'orin', sticker_2
    yield Guild.precreate(202306260031, stickers = [sticker_3]), 'orin', None
    yield Guild.precreate(202306240033, stickers = [sticker_0, sticker_1, sticker_2, sticker_3]), 'rin', sticker_1,
    yield Guild.precreate(202306240034, stickers = [sticker_2, sticker_4]), 'rin', sticker_4


@vampytest._(vampytest.call_from(_iter_options__get_sticker_like()).returning_last())
def test__Guild__get_sticker_like(guild, name):
    """
    Tests whether ``Guild.get_sticker_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the sticker from.
    name : `str`
        Sticker name to query.
    
    Returns
    -------
    output : `None`, ``Sticker``
    """
    return guild.get_sticker_like(name)


def _iter_options__get_stickers_like():
    sticker_0 = Sticker.precreate(202306240048, name = 'orin')
    sticker_1 = Sticker.precreate(202306240049, name = 'rin')
    sticker_2 = Sticker.precreate(202306260020, name = 'cat', tags = ['orin'])
    sticker_3 = Sticker.precreate(202306260022, name = 'cat', tags = ['rin'])
    sticker_4 = Sticker.precreate(202306260024, name = 'cat', tags = ['orin', 'rin'])
    
    yield Guild.precreate(202306240050, stickers = None), 'rin', []
    yield Guild.precreate(202306240051, stickers = [sticker_0]), 'rin', [sticker_0]
    yield Guild.precreate(202306240052, stickers = [sticker_1]), 'rin', [sticker_1]
    yield Guild.precreate(202306240053, stickers = [sticker_1]), 'orin', []
    yield Guild.precreate(202306240054, stickers = [sticker_0, sticker_1]), 'rin', [sticker_1, sticker_0]
    yield Guild.precreate(202306240055, stickers = [sticker_0, sticker_1]), 'orin', [sticker_0]
    yield Guild.precreate(202306240056, stickers = [sticker_0, sticker_1]), 'okuu', []
    yield Guild.precreate(202306260021, stickers = [sticker_2]), 'orin', [sticker_2]
    yield Guild.precreate(202306260022, stickers = [sticker_3]), 'orin', []
    yield (
        Guild.precreate(202306240023, stickers = [sticker_0, sticker_1, sticker_2, sticker_3]),
        'rin',
        [sticker_1, sticker_0, sticker_3, sticker_2],
    )
    yield Guild.precreate(202306240025, stickers = [sticker_2, sticker_4]), 'rin', [sticker_4, sticker_2]


@vampytest._(vampytest.call_from(_iter_options__get_stickers_like()).returning_last())
def test__Guild__get_stickers_like(guild, name):
    """
    Tests whether ``Guild.get_stickers_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the sticker from.
    name : `str`
        Sticker name to query.
    
    Returns
    -------
    output : `list` of ``Sticker``
    """
    return guild.get_stickers_like(name)


def _iter_options__get_role():
    role_0 = Role.precreate(202306240057, name = 'orin')
    role_1 = Role.precreate(202306240058, name = 'rin')
    
    yield Guild.precreate(202306240059, roles = None), 'rin', None
    yield Guild.precreate(202306240060, roles = [role_0]), 'rin', None
    yield Guild.precreate(202306240061, roles = [role_1]), 'rin', role_1
    yield Guild.precreate(202306240062, roles = [role_0, role_1]), 'rin', role_1


@vampytest._(vampytest.call_from(_iter_options__get_role()).returning_last())
def test__Guild__get_role(guild, name):
    """
    Tests whether ``Guild.get_role`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the role from.
    name : `str`
        Role name to query.
    
    Returns
    -------
    output : `None`, ``Role``
    """
    return guild.get_role(name)


def _iter_options__get_role_like():
    role_0 = Role.precreate(202306240063, name = 'orin')
    role_1 = Role.precreate(202306240064, name = 'rin')
    
    yield Guild.precreate(202306240065, roles = None), 'rin', None
    yield Guild.precreate(202306240066, roles = [role_0]), 'rin', role_0
    yield Guild.precreate(202306240067, roles = [role_1]), 'rin', role_1
    yield Guild.precreate(202306240068, roles = [role_1]), 'orin', None
    yield Guild.precreate(202306240069, roles = [role_0, role_1]), 'rin', role_1
    yield Guild.precreate(202306240070, roles = [role_0, role_1]), 'orin', role_0
    yield Guild.precreate(202306240071, roles = [role_0, role_1]), 'okuu', None


@vampytest._(vampytest.call_from(_iter_options__get_role_like()).returning_last())
def test__Guild__get_role_like(guild, name):
    """
    Tests whether ``Guild.get_role_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the role from.
    name : `str`
        Role name to query.
    
    Returns
    -------
    output : `None`, ``Role``
    """
    return guild.get_role_like(name)


def _iter_options__get_roles_like():
    role_0 = Role.precreate(202306240072, name = 'orin')
    role_1 = Role.precreate(202306240073, name = 'rin')
    
    yield Guild.precreate(202306240074, roles = None), 'rin', []
    yield Guild.precreate(202306240075, roles = [role_0]), 'rin', [role_0]
    yield Guild.precreate(202306240076, roles = [role_1]), 'rin', [role_1]
    yield Guild.precreate(202306240077, roles = [role_1]), 'orin', []
    yield Guild.precreate(202306240078, roles = [role_0, role_1]), 'rin', [role_1, role_0]
    yield Guild.precreate(202306240079, roles = [role_0, role_1]), 'orin', [role_0]
    yield Guild.precreate(202306240080, roles = [role_0, role_1]), 'okuu', []


@vampytest._(vampytest.call_from(_iter_options__get_roles_like()).returning_last())
def test__Guild__get_roles_like(guild, name):
    """
    Tests whether ``Guild.get_roles_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the role from.
    name : `str`
        Role name to query.
    
    Returns
    -------
    output : `list` of ``Role``
    """
    return guild.get_roles_like(name)


def _iter_options__get_channel():
    channel_0 = Channel.precreate(202306250003, name = 'orin', channel_type = ChannelType.guild_text)
    channel_1 = Channel.precreate(202306250004, name = 'rin', channel_type = ChannelType.guild_voice)
    channel_2 = Channel.precreate(202306250005, name = 'okuu', channel_type = ChannelType.guild_announcements)
    channel_3 = Channel.precreate(202306250006, name = 'okuu', channel_type = ChannelType.guild_stage)
    
    yield Guild.precreate(202306250007, channels = None), 'rin', None, None
    yield Guild.precreate(202306250008, channels = [channel_0]), 'rin', None, None
    yield Guild.precreate(202306250009, channels = [channel_1]), 'rin', None, channel_1
    yield Guild.precreate(202306250010, channels = [channel_0, channel_1]), 'rin', None, channel_1
    yield Guild.precreate(202306250011, channels = [channel_2, channel_3]), 'OKUU', None, channel_3
    yield (
        Guild.precreate(202306250013, channels = [channel_2, channel_3]),
        'okuu',
        Channel.is_in_group_guild_textual,
        channel_2,
    )
    yield Guild.precreate(202306250014, channels = [channel_0]), 'orin', Channel.is_guild_forum, None


@vampytest._(vampytest.call_from(_iter_options__get_channel()).returning_last())
def test__Guild__get_channel(guild, name, type_checker):
    """
    Tests whether ``Guild.get_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the channel from.
    name : `str`
        Channel name to query.
    type_checker : `None`, `FunctionType`
        Function specifically to check the channel's type.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.get_channel(name, type_checker = type_checker)


def _iter_options__get_channel_like():
    channel_0 = Channel.precreate(202306250015, name = 'orin', channel_type = ChannelType.guild_text)
    channel_1 = Channel.precreate(202306250016, name = 'rin', channel_type = ChannelType.guild_voice)
    channel_2 = Channel.precreate(202306250017, name = 'okuu', channel_type = ChannelType.guild_announcements)
    channel_3 = Channel.precreate(202306250018, name = 'okuu', channel_type = ChannelType.guild_forum)
    
    yield Guild.precreate(202306250019, channels = None), 'rin', None, None
    yield Guild.precreate(202306250020, channels = [channel_0]), 'rin', None, channel_0
    yield Guild.precreate(202306250021, channels = [channel_1]), 'rin', None, channel_1
    yield Guild.precreate(202306250022, channels = [channel_1]), 'orin', None, None
    yield Guild.precreate(202306250023, channels = [channel_0, channel_1]), 'rin', None, channel_1
    yield Guild.precreate(202306250024, channels = [channel_0, channel_1]), 'orin', None, channel_0
    yield Guild.precreate(202306250025, channels = [channel_0, channel_1]), 'okuu', None, None
    yield Guild.precreate(202306250026, channels = [channel_0, channel_2]), 'o', Channel.is_guild_text, channel_0
    yield (
        Guild.precreate(202306250027, channels = [channel_0, channel_2]),
        'o',
        Channel.is_guild_announcements,
        channel_2,
    )
    yield (
        Guild.precreate(202306250028, channels = [channel_2, channel_3]),
        'okuu',
        Channel.is_in_group_guild_textual,
        channel_2,
    )


@vampytest._(vampytest.call_from(_iter_options__get_channel_like()).returning_last())
def test__Guild__get_channel_like(guild, name, type_checker):
    """
    Tests whether ``Guild.get_channel_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the channel from.
    name : `str`
        Channel name to query.
    type_checker : `None`, `FunctionType`
        Function specifically to check the channel's type.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.get_channel_like(name, type_checker = type_checker)


def _iter_options__get_channels_like():
    channel_0 = Channel.precreate(202306250029, name = 'orin', channel_type = ChannelType.guild_text)
    channel_1 = Channel.precreate(202306250030, name = 'rin', channel_type = ChannelType.guild_voice)
    channel_2 = Channel.precreate(202306250031, name = 'okuu', channel_type = ChannelType.guild_announcements)
    channel_3 = Channel.precreate(202306250032, name = 'okuu', channel_type = ChannelType.guild_forum)
    
    yield Guild.precreate(202306250033, channels = None), 'rin', None, []
    yield Guild.precreate(202306250034, channels = [channel_0]), 'rin', None, [channel_0]
    yield Guild.precreate(202306250035, channels = [channel_1]), 'rin', None, [channel_1]
    yield Guild.precreate(202306250036, channels = [channel_1]), 'orin', None, []
    yield Guild.precreate(202306250037, channels = [channel_0, channel_1]), 'rin', None, [channel_1, channel_0]
    yield Guild.precreate(202306250038, channels = [channel_0, channel_1]), 'orin', None, [channel_0]
    yield Guild.precreate(202306250039, channels = [channel_0, channel_1]), 'okuu', None, []
    yield Guild.precreate(202306250040, channels = [channel_0, channel_2]), 'o', Channel.is_guild_text, [channel_0]
    yield (
        Guild.precreate(202306250041, channels = [channel_0, channel_2]),
        'o',
        Channel.is_guild_announcements,
        [channel_2]
    )
    yield (
        Guild.precreate(202306250042, channels = [channel_2, channel_3]),
        'okuu',
        Channel.is_in_group_guild_textual,
        [channel_2],
    )


@vampytest._(vampytest.call_from(_iter_options__get_channels_like()).returning_last())
def test__Guild__get_channels_like(guild, name, type_checker):
    """
    Tests whether ``Guild.get_channels_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the channel from.
    name : `str`
        Channel name to query.
    type_checker : `None`, `FunctionType`
        Function specifically to check the channel's type.
    
    Returns
    -------
    output : `list` of ``Channel``
    """
    return guild.get_channels_like(name, type_checker = type_checker)


def _iter_options__get_user():
    user_0 = User.precreate(202306260023, name = 'orin')
    user_1 = User.precreate(202306260024, name = 'rin')
    user_2 = User.precreate(202306260025, name = 'cat', discriminator = 12, display_name = 'orin')
    user_3 = User.precreate(202306260026, name = 'cat', discriminator = 14)
    user_3_guild_profile = GuildProfile(nick = 'orin')
    
    
    yield Guild.precreate(202306260027, users = None), 'rin', None
    yield Guild.precreate(202306260028, users = [user_0]), 'rin', None
    yield Guild.precreate(202306260029, users = [user_1]), 'rin', user_1
    yield Guild.precreate(202306260030, users = [user_0, user_1]), 'rin', user_1
    yield Guild.precreate(202306260031, users = [user_2]), 'orin', user_2
    yield Guild.precreate(202306260032, users = [user_1, user_2]), 'orin', user_2
    yield Guild.precreate(202306260033, users = [user_0, user_1, user_2]), 'orin', user_0
    
    guild_id = 202306260034
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_3]), 'orin', user_3
    
    guild_id = 202306260035
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_2, user_3]), 'orin', user_2
    
    guild_id = 202306260036
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_0, user_3]), 'orin', user_0
    
    yield Guild.precreate(202306260037, users = [user_2, user_3]), 'cat#0012', user_2
    yield Guild.precreate(202306260038, users = [user_2, user_3]), 'cat#0014', user_3


@vampytest._(vampytest.call_from(_iter_options__get_user()).returning_last())
def test__Guild__get_user(guild, name):
    """
    Tests whether ``Guild.get_user`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the user from.
    name : `str`
        User name to query.
    
    Returns
    -------
    output : `None`, ``ClientUserBase``
    """
    return guild.get_user(name)


def _iter_options__get_user_like():
    user_0 = User.precreate(202306260039, name = 'orin')
    user_1 = User.precreate(202306260040, name = 'rin')
    user_2 = User.precreate(202306260041, name = 'cat', discriminator = 12, display_name = 'orin')
    user_3 = User.precreate(202306260042, name = 'cat', discriminator = 14)
    user_3_guild_profile = GuildProfile(nick = 'orin')
    
    yield Guild.precreate(202306260043, users = None), 'rin', None
    yield Guild.precreate(202306260044, users = [user_0]), 'rin', user_0
    yield Guild.precreate(202306260045, users = [user_1]), 'rin', user_1
    yield Guild.precreate(202306260046, users = [user_1]), 'orin', None
    yield Guild.precreate(202306260047, users = [user_0, user_1, user_2, user_3]), 'rin', user_1
    yield Guild.precreate(202306260048, users = [user_0, user_1]), 'orin', user_0
    
    guild_id = 202306260049
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_0, user_1, user_2, user_3]), 'okuu', None
    
    guild_id = 202306260050
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_3]), 'orin', user_3
    
    guild_id = 202306260051
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_2, user_3]), 'orin', user_2
    
    guild_id = 202306260052
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_0, user_3]), 'orin', user_0
    
    guild_id = 202306260054
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_3]), 'rin', user_3
    
    guild_id = 202306260055
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_2, user_3]), 'rin', user_2
    
    guild_id = 202306260056
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield Guild.precreate(guild_id, users = [user_0, user_3]), 'rin', user_0
    
    yield Guild.precreate(202306260057, users = [user_2, user_3]), 'cat#0012', user_2
    yield Guild.precreate(202306260058, users = [user_2, user_3]), 'cat#0014', user_3


@vampytest._(vampytest.call_from(_iter_options__get_user_like()).returning_last())
def test__Guild__get_user_like(guild, name):
    """
    Tests whether ``Guild.get_user_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the user from.
    name : `str`
        User name to query.
    
    Returns
    -------
    output : `None`, ``ClientUserBase``
    """
    return guild.get_user_like(name)


def _iter_options__get_users_like():
    user_0 = User.precreate(202306260059, name = 'orin')
    user_1 = User.precreate(202306260060, name = 'rin')
    user_2 = User.precreate(202306260061, name = 'cat', discriminator = 12, display_name = 'orin')
    user_3 = User.precreate(202306260062, name = 'cat', discriminator = 14)
    user_3_guild_profile = GuildProfile(nick = 'orin')
    
    yield Guild.precreate(202306260063, users = None), 'rin', []
    yield Guild.precreate(202306260064, users = [user_0]), 'rin', [user_0]
    yield Guild.precreate(202306260065, users = [user_1]), 'rin', [user_1]
    yield Guild.precreate(202306260066, users = [user_1]), 'orin', []
    yield Guild.precreate(202306260067, users = [user_0, user_1]), 'rin', [user_1, user_0]
    yield Guild.precreate(202306260068, users = [user_0, user_1]), 'orin', [user_0]
    yield Guild.precreate(202306260069, users = [user_0, user_1]), 'okuu', []

    guild_id = 202306260070
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield (
        Guild.precreate(guild_id, users = [user_0, user_1, user_2, user_3]),
        'rin',
        [user_1, user_0, user_2, user_3],
    )
    
    guild_id = 202306260071
    user_3.guild_profiles[guild_id] = user_3_guild_profile
    yield (
        Guild.precreate(guild_id, users = [user_0, user_1, user_2, user_3]),
        'orin',
        [user_0, user_2, user_3],
    )
    
    yield Guild.precreate(202306260072, users = [user_2, user_3]), 'cat#0012', [user_2]
    yield Guild.precreate(202306260073, users = [user_2, user_3]), 'cat#0014', [user_3]


@vampytest._(vampytest.call_from(_iter_options__get_users_like()).returning_last())
def test__Guild__get_users_like(guild, name):
    """
    Tests whether ``Guild.get_users_like`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to get the user from.
    name : `str`
        User name to query.
    
    Returns
    -------
    output : `list` of ``ClientUserBase``
    """
    return guild.get_users_like(name)


def _iter_options__get_users_like_ordered():
    guild_id = 202306260074
    
    user_0 = User.precreate(202306260074, name = 'orin')
    user_0.guild_profiles[guild_id] = GuildProfile(joined_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    user_1 = User.precreate(202306260075, name = 'rin')
    user_1.guild_profiles[guild_id] = GuildProfile(joined_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc))
    
    user_2 = User.precreate(202306260076, name = 'cat', discriminator = 12, display_name = 'orin')
    user_2.guild_profiles[guild_id] = GuildProfile(joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc))
    
    user_3 = User.precreate(202306260077, name = 'cat', discriminator = 14)
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'orin', joined_at = DateTime(2016, 5, 12, tzinfo = TimeZone.utc))

    user_4 = User.precreate(202306260078, name = 'cat', discriminator = 14)
    user_4.guild_profiles[guild_id] = GuildProfile(nick = 'okuu', joined_at = DateTime(2016, 5, 20, tzinfo = TimeZone.utc))
    
    guild = Guild.precreate(guild_id, users = [user_0, user_1, user_2, user_3, user_4])
    
    yield guild, 'rin', [user_3, user_1, user_0, user_2]
    yield guild, 'orin', [user_3, user_0, user_2]
    yield guild, 'okuu', [user_4]
    yield guild, 'koishi', []
    yield guild, 'cat', [user_3, user_2, user_4]
    yield guild, 'o', [user_3, user_0, user_2, user_4]


@vampytest._(vampytest.call_from(_iter_options__get_users_like_ordered()).returning_last())
def test__Guild__get_users_like_ordered(guild, name):
    """
    Tests whether ``Guild.get_users_like_ordered`` works as intended.
    """
    return guild.get_users_like_ordered(name)


def _iter_options__iter_users():
    user_0 = User.precreate(202306260000)
    user_1 = User.precreate(202306260001)
    
    yield Guild.precreate(202306260002), set()
    yield Guild.precreate(202306260003, users = [user_0]), {user_0}
    yield Guild.precreate(202306260004, users = [user_0, user_1]), {user_0, user_1}


@vampytest.skip_if(not hasattr(Guild, 'iter_users'))
@vampytest._(vampytest.call_from(_iter_options__iter_users()).returning_last())
def test__Guild__iter_users(guild):
    """
    Tests whether ``Guild.iter_users`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its users of.
    
    Returns
    -------
    output : `set` of ``ClientUserBase``
    """
    return {*guild.iter_users()}


def _iter_options__iter_roles():
    role_0 = Role.precreate(202306260005)
    role_1 = Role.precreate(202306260006)
    
    yield Guild.precreate(202306260007), set()
    yield Guild.precreate(202306260008, roles = [role_0]),  {role_0}
    yield Guild.precreate(202306260009, roles = [role_0, role_1]), {role_0, role_1}


@vampytest.skip_if(not hasattr(Guild, 'iter_roles'))
@vampytest._(vampytest.call_from(_iter_options__iter_roles()).returning_last())
def test__Guild__iter_roles(guild):
    """
    Tests whether ``Guild.iter_roles`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its users of.
    
    Returns
    -------
    output : `set` of ``Role``
    """
    return {*guild.iter_roles()}


def _iter_options__iter_emojis():
    emoji_0 = Emoji.precreate(202306260010)
    emoji_1 = Emoji.precreate(202306260011)
    
    yield Guild.precreate(202306260012), set()
    yield Guild.precreate(202306260013, emojis = [emoji_0]), {emoji_0}
    yield Guild.precreate(202306260014, emojis = [emoji_0, emoji_1]), {emoji_0, emoji_1}


@vampytest.skip_if(not hasattr(Guild, 'iter_emojis'))
@vampytest._(vampytest.call_from(_iter_options__iter_emojis()).returning_last())
def test__Guild__iter_emojis(guild):
    """
    Tests whether ``Guild.iter_emojis`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its emojis of.
    
    Returns
    -------
    output : `set` of ``Emojis``
    """
    return {*guild.iter_emojis()}


def _iter_options__iter_stickers():
    sticker_0 = Sticker.precreate(202306260015)
    sticker_1 = Sticker.precreate(202306260016)
    
    yield Guild.precreate(202306260017), set()
    yield Guild.precreate(202306260018, stickers = [sticker_0]), {sticker_0}
    yield Guild.precreate(202306260019, stickers = [sticker_0, sticker_1]), {sticker_0, sticker_1}


@vampytest.skip_if(not hasattr(Guild, 'iter_stickers'))
@vampytest._(vampytest.call_from(_iter_options__iter_stickers()).returning_last())
def test__Guild__iter_stickers(guild):
    """
    Tests whether ``Guild.iter_stickers`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its stickers of.
    
    Returns
    -------
    output : `set` of ``Sticker``
    """
    return {*guild.iter_stickers()}


def _iter_options__iter_channels():
    channel_0 = Channel.precreate(202306270000, channel_type = ChannelType.guild_text)
    channel_1 = Channel.precreate(202306270001, channel_type = ChannelType.guild_forum)
    channel_2 = Channel.precreate(202306270002, channel_type = ChannelType.guild_announcements)
    
    yield Guild.precreate(202306270003), None, set()
    yield Guild.precreate(202306270004, channels = [channel_0]), None, {channel_0}
    yield Guild.precreate(202306270005, channels = [channel_0, channel_1]), None, {channel_0, channel_1}
    yield (
        Guild.precreate(202306270006, channels = [channel_0, channel_1, channel_2]),
        Channel.is_in_group_guild_textual,
        {channel_0, channel_2},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_channels()).returning_last())
def test__Guild__iter_channels(guild, type_checker):
    """
    Tests whether ``Guild.iter_channels`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its channels of.
    type_checker : `None`, `FunctionType`
        Function specifically to check the channel's type.
    
    Returns
    -------
    output : `set` of ``Channel``
    """
    return {*guild.iter_channels(type_checker)}


def _iter_options__iter_scheduled_events():
    scheduled_event_0 = ScheduledEvent.precreate(202306270007)
    scheduled_event_1 = ScheduledEvent.precreate(202306270008)
    
    yield Guild.precreate(202306270009), set()
    yield Guild.precreate(202306270010, scheduled_events = [scheduled_event_0]), {scheduled_event_0}
    yield (
        Guild.precreate(202306270011, scheduled_events = [scheduled_event_0, scheduled_event_1]),
        {scheduled_event_0, scheduled_event_1}
    )


@vampytest._(vampytest.call_from(_iter_options__iter_scheduled_events()).returning_last())
def test__Guild__iter_scheduled_events(guild):
    """
    Tests whether ``Guild.iter_scheduled_events`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its scheduled events of.
    
    Returns
    -------
    output : `set` of ``ScheduledEvent``
    """
    return {*guild.iter_scheduled_events()}


def _iter_options__iter_embedded_activity_states():
    embedded_activity_state_0 = EmbeddedActivityState(
        activity = Activity('dance'), guild_id = 202306270012, channel_id = 202306270013
    )
    embedded_activity_state_1 = EmbeddedActivityState(
        activity = Activity('party'), guild_id = 202306270014, channel_id = 202306270015
    )

    yield Guild.precreate(202306270016), set()
    yield (
        Guild.precreate(202306270017, embedded_activity_states = [embedded_activity_state_0]),
        {embedded_activity_state_0},
    )
    yield (
        Guild.precreate(202306270018, embedded_activity_states = [embedded_activity_state_0, embedded_activity_state_1]),
        {embedded_activity_state_0, embedded_activity_state_1}
    )


@vampytest._(vampytest.call_from(_iter_options__iter_embedded_activity_states()).returning_last())
def test__Guild__iter_embedded_activity_states(guild):
    """
    Tests whether ``Guild.iter_embedded_activity_states`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its embedded activity states of.
    
    Returns
    -------
    output : `set` of ``EmbeddedActivityState``
    """
    return {*guild.iter_embedded_activity_states()}


def _iter_options__iter_stages():
    stage_0 = Stage.precreate(202306270019)
    stage_1 = Stage.precreate(202306270020)
    
    yield Guild.precreate(202306270021), set()
    yield Guild.precreate(202306270022, stages = [stage_0]), {stage_0}
    yield Guild.precreate(202306270023, stages = [stage_0, stage_1]), {stage_0, stage_1}


@vampytest._(vampytest.call_from(_iter_options__iter_stages()).returning_last())
def test__Guild__iter_stages(guild):
    """
    Tests whether ``Guild.iter_stages`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its stages of.
    
    Returns
    -------
    output : `set` of ``Stage``
    """
    return {*guild.iter_stages()}


def _iter_options__iter_threads():
    thread_0 = Channel.precreate(202306270024)
    thread_1 = Channel.precreate(202306270025)
    
    yield Guild.precreate(202306270026), set()
    yield Guild.precreate(202306270027, threads = [thread_0]), {thread_0}
    yield Guild.precreate(202306270028, threads = [thread_0, thread_1]), {thread_0, thread_1}


@vampytest._(vampytest.call_from(_iter_options__iter_threads()).returning_last())
def test__Guild__iter_threads(guild):
    """
    Tests whether ``Guild.iter_threads`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its threads of.
    
    Returns
    -------
    output : `set` of ``Channel``
    """
    return {*guild.iter_threads()}


def _iter_options__iter_voice_states():
    voice_state_0 = VoiceState(user_id = 202306270029)
    voice_state_1 = VoiceState(user_id = 202306270030)
    
    yield Guild.precreate(202306270030), set()
    yield Guild.precreate(202306270031, voice_states = [voice_state_0]), {voice_state_0}
    yield Guild.precreate(202306270032, voice_states = [voice_state_0, voice_state_1]), {voice_state_0, voice_state_1}


@vampytest._(vampytest.call_from(_iter_options__iter_voice_states()).returning_last())
def test__Guild__iter_voice_states(guild):
    """
    Tests whether ``Guild.iter_voice_states`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its voice states of.
    
    Returns
    -------
    output : `set` of ``VoiceState``
    """
    return {*guild.iter_voice_states()}


def _iter_options__afk_channel():
    yield Guild.precreate(202306270033), None
    
    channel_id = 202306270034
    yield Guild.precreate(202306270035, afk_channel_id = channel_id), None
    
    channel_id = 202306270036
    channel = Channel.precreate(channel_id)
    yield Guild.precreate(202306270037, afk_channel_id = channel_id, channels = [channel]), channel
    

@vampytest._(vampytest.call_from(_iter_options__afk_channel()).returning_last())
def test__Guild__afk_channel(guild):
    """
    Tests whether ``Guild.afk_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its afk channel of.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.afk_channel


def _iter_options__rules_channel():
    yield Guild.precreate(202306270038), None
    
    channel_id = 202306270039
    yield Guild.precreate(202306270040, rules_channel_id = channel_id), None
    
    channel_id = 202306270041
    channel = Channel.precreate(channel_id)
    yield Guild.precreate(202306270042, rules_channel_id = channel_id, channels = [channel]), channel
    

@vampytest._(vampytest.call_from(_iter_options__rules_channel()).returning_last())
def test__Guild__rules_channel(guild):
    """
    Tests whether ``Guild.rules_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its afk channel of.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.rules_channel


def _iter_options__safety_alerts_channel():
    yield Guild.precreate(202306270043), None
    
    channel_id = 202306270044
    yield Guild.precreate(202306270045, safety_alerts_channel_id = channel_id), None
    
    channel_id = 202306270046
    channel = Channel.precreate(channel_id)
    yield Guild.precreate(202306270047, safety_alerts_channel_id = channel_id, channels = [channel]), channel
    

@vampytest._(vampytest.call_from(_iter_options__safety_alerts_channel()).returning_last())
def test__Guild__safety_alerts_channel(guild):
    """
    Tests whether ``Guild.safety_alerts_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its afk channel of.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.safety_alerts_channel


def _iter_options__system_channel():
    yield Guild.precreate(202306270048), None
    
    channel_id = 202306270049
    yield Guild.precreate(202306270050, system_channel_id = channel_id), None
    
    channel_id = 202306270051
    channel = Channel.precreate(channel_id)
    yield Guild.precreate(202306270052, system_channel_id = channel_id, channels = [channel]), channel
    

@vampytest._(vampytest.call_from(_iter_options__system_channel()).returning_last())
def test__Guild__system_channel(guild):
    """
    Tests whether ``Guild.system_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its afk channel of.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.system_channel


def _iter_options__widget_channel():
    yield Guild.precreate(202306270053), None
    
    channel_id = 202306270054
    yield Guild.precreate(202306270055, widget_channel_id = channel_id), None
    
    channel_id = 202306270056
    channel = Channel.precreate(channel_id)
    yield Guild.precreate(202306270057, widget_channel_id = channel_id, channels = [channel]), channel
    

@vampytest._(vampytest.call_from(_iter_options__widget_channel()).returning_last())
def test__Guild__widget_channel(guild):
    """
    Tests whether ``Guild.widget_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to get its afk channel of.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return guild.widget_channel


def test__Guild__channel_list():
    """
    Tests whether ``Guild.channel_list`` works as intended.
    """
    guild_id = 202306270058
    
    channel_0 = Channel.precreate(
        202306270059, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 4
    )
    channel_1 = Channel.precreate(
        202306270060, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 2
    )
    channel_2 = Channel.precreate(
        202306270061, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 3
    )
    channel_3 = Channel.precreate(
        202306270062, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 3
    )
    channel_4 = Channel.precreate(
        202306270063, guild_id = guild_id, channel_type = ChannelType.guild_category, position = 5
    )
    channel_5 = Channel.precreate(
        202306270064, guild_id = guild_id, channel_type = ChannelType.guild_category, position = 0
    )
    channel_6 = Channel.precreate(
        202306270065, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 7, parent_id = channel_5.id
    )
    channel_7 = Channel.precreate(
        202306270066, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 6, parent_id = channel_5.id
    )
    channel_8 = Channel.precreate(
        202306270067, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 4, parent_id = channel_5.id
    )
    channel_9 = Channel.precreate(
        202306270068, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 4, parent_id = channel_5.id
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [
            channel_0, channel_1, channel_2, channel_3, channel_4, channel_5, channel_6, channel_7, channel_8, channel_9
        ]
    )
    
    channel_list = guild.channel_list
    vampytest.assert_instance(channel_list, list)
    vampytest.assert_eq(
        channel_list,
        [
            channel_1,
            channel_0,
            channel_2,
            channel_3,
            channel_5,
            channel_4,
        ],
    )


def test__Guild__channel_list_flattened():
    """
    Tests whether ``Guild.channel_list_flattened`` works as intended.
    """
    guild_id = 202306270069
    
    channel_0 = Channel.precreate(
        202306270070, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 4
    )
    channel_1 = Channel.precreate(
        202306270071, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 2
    )
    channel_2 = Channel.precreate(
        202306270072, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 3
    )
    channel_3 = Channel.precreate(
        202306270073, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 3
    )
    channel_4 = Channel.precreate(
        202306270074, guild_id = guild_id, channel_type = ChannelType.guild_category, position = 5
    )
    channel_5 = Channel.precreate(
        202306270075, guild_id = guild_id, channel_type = ChannelType.guild_category, position = 0
    )
    channel_6 = Channel.precreate(
        202306270076, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 7, parent_id = channel_5.id
    )
    channel_7 = Channel.precreate(
        202306270077, guild_id = guild_id, channel_type = ChannelType.guild_text, position = 6, parent_id = channel_5.id
    )
    channel_8 = Channel.precreate(
        202306270078, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 4, parent_id = channel_5.id
    )
    channel_9 = Channel.precreate(
        202306270079, guild_id = guild_id, channel_type = ChannelType.guild_voice, position = 4, parent_id = channel_5.id
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [
            channel_0, channel_1, channel_2, channel_3, channel_4, channel_5, channel_6, channel_7, channel_8, channel_9
        ]
    )
    
    channel_list = guild.channel_list_flattened
    vampytest.assert_instance(channel_list, list)
    vampytest.assert_eq(
        channel_list,
        [
            channel_1,
            channel_0,
            channel_2,
            channel_3,
            channel_5,
            channel_7,
            channel_6,
            channel_8,
            channel_9,
            channel_4,
        ],
    )


def test__Guild__role_list():
    """
    Tests whether ``Guild.role_list`` works as intended.
    """
    guild_id = 202306270082
    
    role_0 = Role.precreate(202306270083, guild_id = guild_id, position = 2)
    role_1 = Role.precreate(202306270084, guild_id = guild_id, position = 2)
    role_2 = Role.precreate(202306270085, guild_id = guild_id, position = 1)

    guild = Guild.precreate(guild_id, roles = [role_0, role_1, role_2])
    
    role_list = guild.role_list
    vampytest.assert_instance(role_list, list)
    vampytest.assert_eq(
        role_list,
        [
            role_2,
            role_0,
            role_1,
        ],
    )


def test__Guild__clear_cache():
    """
    Tests whether ``Guild._clear_cache`` works as intended.
    """
    guild = Guild.precreate(202306270086)
    guild._state = GUILD_STATE_MASK_CACHE_ALL
    guild._cache_boosters = (User.precreate(202306270087),)
    
    guild._clear_cache()
    
    vampytest.assert_eq(guild._state, 0)
    vampytest.assert_is(guild._cache_boosters, None)


def test__Guild__boosters__has():
    """
    Tests whether ``Guild.boosters`` works as intended.
    
    Case : Has boosters.
    """
    guild_id = 202306270091
    
    user_0 = User.precreate(202306270088)
    user_0.guild_profiles[guild_id] = GuildProfile()
    
    user_1 = User.precreate(202306270089)
    user_1.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2016, 4, 14, tzinfo = TimeZone.utc))
    
    user_2 = User.precreate(202306270090)
    
    user_3 = User.precreate(202306270092)
    user_3.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2015, 4, 14, tzinfo = TimeZone.utc))
    
    guild = Guild.precreate(guild_id, users = [user_0, user_1, user_2, user_3], boost_count = 2)
    
    boosters = guild.boosters
    vampytest.assert_instance(boosters, tuple, nullable = True)
    vampytest.assert_eq(boosters, (user_3, user_1))
    
    vampytest.assert_true(guild._state & GUILD_STATE_MASK_CACHE_BOOSTERS)
    vampytest.assert_is(guild.boosters, boosters)
    

def test__Guild__boosters__none():
    """
    Tests whether ``Guild.boosters`` works as intended.
    
    Case: No boosters.
    """
    guild = Guild.precreate(202306270093)
    
    boosters = guild.boosters
    vampytest.assert_instance(boosters, tuple, nullable = True)
    vampytest.assert_eq(boosters, None)
    
    vampytest.assert_true(guild._state & GUILD_STATE_MASK_CACHE_BOOSTERS)
    vampytest.assert_is(guild.boosters, boosters)


def test__Guild__permissions_for__owner():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: owner.
    """
    guild_id = 202306270094
    user_id = 202306270095
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    guild = Guild.precreate(guild_id, owner_id = user_id, users = [user])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_ALL)


def test__Guild__permissions_for__admin():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: admin.
    """
    guild_id = 202306270096
    user_id = 202306270097
    role_id = 202306270098
    default_permissions = Permission().update_by_keys(administrator = True)
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    role = Role.precreate(role_id, permissions = default_permissions)
    guild = Guild.precreate(guild_id, users = [user], roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_ALL)


def test__Guild__permissions_for__webhook_in_default():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: webhook in.
    """
    guild_id = 202306270099
    user_id = 202306270100
    channel_id = 202306270101
    default_permissions = Permission().update_by_keys(ban_users = True)
    
    user = Webhook.precreate(user_id, channel_id = channel_id)
    role = Role.precreate(guild_id, permissions = default_permissions)
    channel = Channel.precreate(channel_id)
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, default_permissions)
    

def test__Guild__permissions_for__webhook_out():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: webhook out.
    """
    guild_id = 202306270102
    user_id = 202306270103
    channel_id = 202306270104
    default_permissions = Permission().update_by_keys(ban_users = True)
    
    user = Webhook.precreate(user_id, channel_id = channel_id)
    role = Role.precreate(guild_id, permissions = default_permissions)
    guild = Guild.precreate(guild_id, roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_NONE)
    

def test__Guild__permissions_for__webhook_in_admin():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: webhook in, default role has admin permissions.
    """
    guild_id = 202306270105
    user_id = 202306270106
    channel_id = 202306270107
    default_permissions = Permission().update_by_keys(administrator = True)
    
    user = Webhook.precreate(user_id, channel_id = channel_id)
    role = Role.precreate(guild_id, permissions = default_permissions)
    channel = Channel.precreate(channel_id)
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_ALL)


def test__Guild__permissions_for__webhook_in_no_default_role():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: webhook in, no default role.
    """
    guild_id = 202306270108
    user_id = 202306270109
    channel_id = 202306270110
    
    user = Webhook.precreate(user_id, channel_id = channel_id)
    channel = Channel.precreate(channel_id)
    guild = Guild.precreate(guild_id, channels = [channel])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_NONE)


def test__Guild__permissions_for__no_default_role():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: no default role.
    """
    guild_id = 202306270111
    user_id = 202306270112
    
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id, users = [user])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_NONE)


def test__Guild__permissions_for__default():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: default role only.
    """
    guild_id = 202306270113
    user_id = 202306270114
    default_permissions = Permission().update_by_keys(ban_users = True)
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    role = Role.precreate(guild_id, permissions = default_permissions)
    guild = Guild.precreate(guild_id, users = [user], roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, default_permissions)


def test__Guild__permissions_for__multiple_roles():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: multiple roles. With missing and extra role too.
    """
    guild_id = 202306270115
    user_id = 202306270116
    role_id_0 = guild_id
    role_id_1 = 202306270117
    role_id_2 = 202306270118
    role_id_3 = 202306270119
    role_id_4 = 202306270120
    
    permissions_0 = Permission().update_by_keys(moderate_users = True)
    permissions_1 = Permission().update_by_keys(ban_users = True)
    permissions_2 = Permission().update_by_keys(kick_users = True)
    permissions_3 = Permission().update_by_keys(stream = True)
    permissions_4 = Permission().update_by_keys(speak = True)
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_1, role_id_2, role_id_4])
    
    role_0 = Role.precreate(role_id_0, permissions = permissions_0)
    role_1 = Role.precreate(role_id_1, permissions = permissions_1)
    role_2 = Role.precreate(role_id_2, permissions = permissions_2)
    role_3 = Role.precreate(role_id_3, permissions = permissions_3)
    role_4 = Role.precreate(role_id_4, permissions = permissions_4)
    
    guild = Guild.precreate(guild_id, users = [user], roles = [role_0, role_1, role_2, role_3])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, permissions_0 | permissions_1 | permissions_2)


def test__Guild__permissions_for__missing():
    """
    Tests whether ``Guild.permissions_for`` works as intended.
    
    Case: missing user.
    """
    guild_id = 202306270121
    user_id = 202306270122
    default_permissions = Permission().update_by_keys(ban_users = True)
    
    user = User.precreate(user_id)
    role = Role.precreate(guild_id, permissions = default_permissions)
    guild = Guild.precreate(guild_id, roles = [role])
    
    permissions = guild.permissions_for(user)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_NONE)


def test__Guild__cached_permissions_for():
    """
    Tests whether ``Guild.cached_permissions_for`` works as intended.
    """
    guild_id = 202306270123
    user_id = 202306270124
    default_permissions = Permission().update_by_keys(moderate_users = True)
    
    client = Client(
        token = 'token_20230626_0000',
        client_id = user_id,
    )
    client.guild_profiles[guild_id] = GuildProfile()
    role = Role.precreate(guild_id, permissions = default_permissions)
    
    guild = Guild.precreate(guild_id, users = [client], roles = [role])
    
    try:
        
        permissions = guild.cached_permissions_for(client)
        vampytest.assert_instance(permissions, Permission)
        vampytest.assert_eq(permissions, default_permissions)
        
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Guild__permissions_for_roles__no_default():
    """
    Tests whether ``Guild.permissions_for_roles`` works as intended.
    
    Case: No default role.
    """
    guild_id = 202306270125
    
    guild = Guild.precreate(guild_id)
    
    permissions = guild.permissions_for_roles()
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_NONE)


def test__Guild__permissions_for_roles__with_default():
    """
    Tests whether ``Guild.permissions_for_roles`` works as intended.
    
    Case: Roles and default role. Extra roles are given too.
    """
    guild_id = 202306270126
    role_id_0 = guild_id
    role_id_1 = 202306270127
    role_id_2 = 202306270128
    role_id_3 = 202306270129
    role_id_4 = 202306270130
    
    permissions_0 = Permission().update_by_keys(moderate_users = True)
    permissions_1 = Permission().update_by_keys(ban_users = True)
    permissions_2 = Permission().update_by_keys(kick_users = True)
    permissions_3 = Permission().update_by_keys(stream = True)
    permissions_4 = Permission().update_by_keys(speak = True)
    
    role_0 = Role.precreate(role_id_0, permissions = permissions_0)
    role_1 = Role.precreate(role_id_1, permissions = permissions_1)
    role_2 = Role.precreate(role_id_2, permissions = permissions_2)
    role_3 = Role.precreate(role_id_3, permissions = permissions_3)
    role_4 = Role.precreate(role_id_4, guild_id = guild_id, permissions = permissions_4)
    
    guild = Guild.precreate(guild_id, roles = [role_0, role_1, role_2, role_3])
    
    permissions = guild.permissions_for_roles(role_1, role_2, role_4)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, permissions_0 | permissions_1 | permissions_2)


def test__Guild__permissions_for_roles__admin():
    """
    Tests whether ``Guild.permissions_for_roles`` works as intended.
    
    Case: No default role.
    """
    guild_id = 202306270131
    role_id = 202306270132
    
    role = Role.precreate(role_id, permissions = Permission().update_by_keys(administrator = True))
    guild = Guild.precreate(guild_id, roles = [role])
    
    permissions = guild.permissions_for_roles(role)
    vampytest.assert_instance(permissions, Permission)
    vampytest.assert_eq(permissions, PERMISSION_ALL)


def _iter_options__get_voice_state():
    user_id_0 = 202407110000
    user_id_1 = 202407110001
    
    voice_state_0 = VoiceState(user_id = user_id_0)
    voice_state_1 = VoiceState(user_id = user_id_1)
    
    yield Guild.precreate(202407110002), user_id_0, None
    yield Guild.precreate(202407110003, voice_states = [voice_state_0]), user_id_0, voice_state_0
    yield Guild.precreate(202407110004, voice_states = [voice_state_1]), user_id_0, None
    yield Guild.precreate(202407110005, voice_states = [voice_state_0, voice_state_1]), user_id_0, voice_state_0


@vampytest._(vampytest.call_from(_iter_options__get_voice_state()).returning_last())
def test__Guild__get_voice_state(guild, user_id):
    """
    Tests whether ``Guild.get_voice_state`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its voice states of.
    user_id : `int`
        User identifier to get voice state for.
    
    Returns
    -------
    output : `None`, ``VoiceState``
    """
    output = guild.get_voice_state(user_id)
    vampytest.assert_instance(output, VoiceState, nullable = True)
    return output
